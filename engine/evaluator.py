"""
PromptPulse Studio - Deterministic Prompt Regression & Evaluation Engine
Version: 1.0.0
Author: PromptPulse Team
License: MIT
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ModelPricing:
    name: str
    input_per_million: float
    output_per_million: float

    def calculate_cost(self, input_tokens: int, output_tokens: int, query_volume: int = 1_000_000) -> float:
        """Calculate total dollar cost for a given query volume."""
        in_cost = (input_tokens / 1_000_000) * self.input_per_million * query_volume
        out_cost = (output_tokens / 1_000_000) * self.output_per_million * query_volume
        return round(in_cost + out_cost, 4)


# Reference pricing models (Q3 2026 rates)
STANDARD_MODELS = {
    "gpt-4o": ModelPricing("OpenAI GPT-4o", 2.50, 10.00),
    "claude-3-5-sonnet": ModelPricing("Anthropic Claude 3.5 Sonnet", 3.00, 15.00),
    "gemini-1-5-pro": ModelPricing("Google Gemini 1.5 Pro", 1.25, 5.00),
    "gemini-1-5-flash": ModelPricing("Google Gemini 1.5 Flash", 0.075, 0.30),
}


@dataclass
class TestCase:
    id: str
    name: str
    description: str
    variables: Dict[str, str]
    expected_schema: Optional[Dict[str, str]] = None  # Key -> expected type string ("string", "number", "list", "dict")
    forbidden_terms: List[str] = field(default_factory=list)
    required_terms: List[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    test_id: str
    test_name: str
    prompt_a_tokens: int
    prompt_b_tokens: int
    token_delta_pct: float
    prompt_a_valid_json: bool
    prompt_b_valid_json: bool
    schema_compliance_a: bool
    schema_compliance_b: bool
    quality_score_a: float
    quality_score_b: float
    regression_detected: bool
    verdict: str  # "PASS", "IMPROVEMENT", "WARNING", "REGRESSION"
    notes: List[str]


class PromptEvaluator:
    """
    Deterministic Local-First Prompt Evaluation Engine.
    Executes prompt template variable interpolation, tokenization approximation,
    schema adherence checks, and comparative regression scoring.
    """

    VARIABLE_REGEX = re.compile(r"\{\{([a-zA-Z0-9_]+)\}\}")

    def __init__(self, models: Optional[Dict[str, ModelPricing]] = None):
        self.models = models or STANDARD_MODELS

    @classmethod
    def extract_variables(cls, template: str) -> List[str]:
        """Extract all unique {{variable}} names from a template string."""
        return sorted(list(set(cls.VARIABLE_REGEX.findall(template))))

    @classmethod
    def interpolate(cls, template: str, variables: Dict[str, str]) -> str:
        """Replace {{variable}} with provided values, leaving missing as empty string."""
        def replacer(match):
            var_name = match.group(1)
            return variables.get(var_name, f"{{{{{var_name}}}}}")
        return cls.VARIABLE_REGEX.sub(replacer, template)

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Estimate token count using BPE character approximation (~4 chars per token)
        plus word-boundary heuristic. Minimum 1 token for non-empty text.
        """
        if not text.strip():
            return 0
        char_tokens = len(text) / 4.0
        word_tokens = len(text.split()) * 1.3
        return max(1, int(round((char_tokens + word_tokens) / 2.0)))

    @staticmethod
    def validate_json_schema(output_text: str, expected_schema: Dict[str, str]) -> Tuple[bool, bool, List[str]]:
        """
        Validates if output is valid JSON and contains required keys with correct types.
        Returns (is_valid_json, is_schema_compliant, errors).
        """
        errors = []
        clean_text = output_text.strip()
        # Strip markdown fences if present
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()

        try:
            data = json.loads(clean_text)
        except Exception as e:
            return False, False, [f"Invalid JSON syntax: {str(e)}"]

        if not isinstance(data, dict):
            return True, False, ["JSON output is not an object/dict"]

        schema_compliant = True
        for key, expected_type in expected_schema.items():
            if key not in data:
                schema_compliant = False
                errors.append(f"Missing required key: '{key}'")
                continue
            
            val = data[key]
            if expected_type == "string" and not isinstance(val, str):
                schema_compliant = False
                errors.append(f"Key '{key}' expected string, got {type(val).__name__}")
            elif expected_type == "number" and not isinstance(val, (int, float)):
                schema_compliant = False
                errors.append(f"Key '{key}' expected number, got {type(val).__name__}")
            elif expected_type == "list" and not isinstance(val, list):
                schema_compliant = False
                errors.append(f"Key '{key}' expected list, got {type(val).__name__}")
            elif expected_type == "dict" and not isinstance(val, dict):
                schema_compliant = False
                errors.append(f"Key '{key}' expected dict, got {type(val).__name__}")

        return True, schema_compliant, errors

    def evaluate_case(
        self,
        test_case: TestCase,
        prompt_a_template: str,
        prompt_b_template: str,
        simulated_output_a: str,
        simulated_output_b: str
    ) -> EvaluationResult:
        """
        Evaluate a single test case comparing Prompt A against Prompt B.
        """
        notes = []

        # 1. Token Estimation
        full_prompt_a = self.interpolate(prompt_a_template, test_case.variables)
        full_prompt_b = self.interpolate(prompt_b_template, test_case.variables)

        tokens_a = self.estimate_tokens(full_prompt_a) + self.estimate_tokens(simulated_output_a)
        tokens_b = self.estimate_tokens(full_prompt_b) + self.estimate_tokens(simulated_output_b)

        token_delta_pct = round(((tokens_b - tokens_a) / max(1, tokens_a)) * 100, 2)

        # 2. Schema Validation
        valid_json_a, schema_comp_a, errors_a = True, True, []
        valid_json_b, schema_comp_b, errors_b = True, True, []

        if test_case.expected_schema:
            valid_json_a, schema_comp_a, errors_a = self.validate_json_schema(simulated_output_a, test_case.expected_schema)
            valid_json_b, schema_comp_b, errors_b = self.validate_json_schema(simulated_output_b, test_case.expected_schema)

        # 3. Quality Scoring (0 - 100)
        score_a = 100.0
        score_b = 100.0

        if test_case.expected_schema:
            if not valid_json_a:
                score_a -= 40.0
            elif not schema_comp_a:
                score_a -= 20.0 * min(2, len(errors_a))

            if not valid_json_b:
                score_b -= 40.0
            elif not schema_comp_b:
                score_b -= 20.0 * min(2, len(errors_b))

        # Check required terms
        for req in test_case.required_terms:
            if req.lower() not in simulated_output_a.lower():
                score_a -= 15.0
            if req.lower() not in simulated_output_b.lower():
                score_b -= 15.0

        # Check forbidden terms
        for forb in test_case.forbidden_terms:
            if forb.lower() in simulated_output_a.lower():
                score_a -= 25.0
            if forb.lower() in simulated_output_b.lower():
                score_b -= 25.0

        # Token inflation penalty if > 25% larger without schema benefit
        if token_delta_pct > 25.0 and score_b <= score_a:
            score_b -= min(15.0, (token_delta_pct - 25.0) * 0.5)

        score_a = max(0.0, min(100.0, round(score_a, 1)))
        score_b = max(0.0, min(100.0, round(score_b, 1)))

        # 4. Regression Determination
        regression_detected = False
        verdict = "PASS"

        if schema_comp_a and not schema_comp_b:
            regression_detected = True
            verdict = "REGRESSION"
            notes.append("Schema regression: Prompt B broke output JSON schema compliance.")
        elif valid_json_a and not valid_json_b:
            regression_detected = True
            verdict = "REGRESSION"
            notes.append("Syntax regression: Prompt B generated invalid JSON.")
        elif score_b < (score_a - 10.0):
            regression_detected = True
            verdict = "REGRESSION"
            notes.append(f"Quality regression: Score dropped from {score_a} to {score_b}.")
        elif token_delta_pct > 40.0 and score_b <= score_a:
            verdict = "WARNING"
            notes.append(f"Severe token inflation: +{token_delta_pct}% token consumption without quality gain.")
        elif score_b > score_a:
            verdict = "IMPROVEMENT"
            notes.append(f"Quality improvement: Score increased from {score_a} to {score_b}.")
        else:
            verdict = "PASS"
            notes.append("Consistent execution within acceptable variance thresholds.")

        return EvaluationResult(
            test_id=test_case.id,
            test_name=test_case.name,
            prompt_a_tokens=tokens_a,
            prompt_b_tokens=tokens_b,
            token_delta_pct=token_delta_pct,
            prompt_a_valid_json=valid_json_a,
            prompt_b_valid_json=valid_json_b,
            schema_compliance_a=schema_comp_a,
            schema_compliance_b=schema_comp_b,
            quality_score_a=score_a,
            quality_score_b=score_b,
            regression_detected=regression_detected,
            verdict=verdict,
            notes=notes
        )

    def calculate_cost_matrix(self, total_tokens_a: int, total_tokens_b: int, query_volume: int = 1_000_000) -> Dict[str, Any]:
        """
        Calculate cost projection across all standard models for a given query volume.
        """
        matrix = {}
        for key, model in self.models.items():
            # Assume 60% prompt input tokens, 40% completion output tokens
            in_a = int(total_tokens_a * 0.6)
            out_a = int(total_tokens_a * 0.4)
            in_b = int(total_tokens_b * 0.6)
            out_b = int(total_tokens_b * 0.4)

            cost_a = model.calculate_cost(in_a, out_a, query_volume)
            cost_b = model.calculate_cost(in_b, out_b, query_volume)
            delta = round(cost_b - cost_a, 2)
            delta_pct = round(((cost_b - cost_a) / max(0.01, cost_a)) * 100, 2)

            matrix[key] = {
                "model_name": model.name,
                "cost_a_usd": cost_a,
                "cost_b_usd": cost_b,
                "delta_usd": delta,
                "delta_pct": delta_pct,
                "status": "SAVINGS" if delta < 0 else ("INFLATION" if delta > 0 else "NEUTRAL")
            }
        return matrix
