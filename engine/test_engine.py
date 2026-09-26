"""
Unit Tests for PromptPulse Studio Evaluation Engine
Deterministic verification of token counting, schema validation, regression detection, and cost models.
Works with both pytest and standard python3 -m unittest.
"""

import unittest
from promptpulse.engine.evaluator import (
    PromptEvaluator,
    ModelPricing,
    TestCase,
    STANDARD_MODELS
)


class TestPromptEvaluator(unittest.TestCase):

    def setUp(self):
        self.evaluator = PromptEvaluator()

    def test_extract_variables(self):
        template = "Hello {{user_name}}, please summarize {{document_text}} in {{max_words}} words."
        vars_found = self.evaluator.extract_variables(template)
        self.assertEqual(vars_found, ["document_text", "max_words", "user_name"])

        # Test duplicates and no variables
        dup_template = "{{query}} is {{query}} again."
        self.assertEqual(self.evaluator.extract_variables(dup_template), ["query"])

        empty_template = "Static system prompt with no variables."
        self.assertEqual(self.evaluator.extract_variables(empty_template), [])

    def test_interpolation(self):
        template = "User: {{user_name}}, Query: {{query}}"
        data = {"user_name": "Alice", "query": "Find flight to NYC"}
        interpolated = self.evaluator.interpolate(template, data)
        self.assertEqual(interpolated, "User: Alice, Query: Find flight to NYC")

        # Test missing variable retention
        partial_data = {"user_name": "Bob"}
        partial = self.evaluator.interpolate(template, partial_data)
        self.assertEqual(partial, "User: Bob, Query: {{query}}")

    def test_estimate_tokens(self):
        self.assertEqual(self.evaluator.estimate_tokens(""), 0)
        self.assertEqual(self.evaluator.estimate_tokens("   "), 0)

        short_text = "Hello world"
        tokens = self.evaluator.estimate_tokens(short_text)
        self.assertTrue(2 <= tokens <= 4)

        long_text = "The quick brown fox jumps over the lazy dog. " * 10
        tokens_long = self.evaluator.estimate_tokens(long_text)
        self.assertTrue(tokens_long > 80)

    def test_validate_json_schema(self):
        schema = {"status": "string", "code": "number", "items": "list"}

        # Perfect match
        valid_json = '{"status": "success", "code": 200, "items": ["a", "b"]}'
        is_valid, is_compliant, errors = self.evaluator.validate_json_schema(valid_json, schema)
        self.assertTrue(is_valid)
        self.assertTrue(is_compliant)
        self.assertEqual(errors, [])

        # Markdown wrapped json
        markdown_json = '```json\n{"status": "ok", "code": 201, "items": []}\n```'
        is_valid, is_compliant, errors = self.evaluator.validate_json_schema(markdown_json, schema)
        self.assertTrue(is_valid)
        self.assertTrue(is_compliant)

        # Missing key
        missing_key_json = '{"status": "error", "code": 404}'
        is_valid, is_compliant, errors = self.evaluator.validate_json_schema(missing_key_json, schema)
        self.assertTrue(is_valid)
        self.assertFalse(is_compliant)
        self.assertTrue(any("items" in e for e in errors))

        # Wrong type
        wrong_type_json = '{"status": 123, "code": "bad_code", "items": "not_a_list"}'
        is_valid, is_compliant, errors = self.evaluator.validate_json_schema(wrong_type_json, schema)
        self.assertTrue(is_valid)
        self.assertFalse(is_compliant)
        self.assertEqual(len(errors), 3)

        # Syntax error
        broken_json = '{"status": "unclosed_string'
        is_valid, is_compliant, errors = self.evaluator.validate_json_schema(broken_json, schema)
        self.assertFalse(is_valid)
        self.assertFalse(is_compliant)

    def test_evaluate_case_pass(self):
        tc = TestCase(
            id="tc-1",
            name="Structured Triage",
            description="Extract urgency and tags",
            variables={"query": "Server down in us-east-1"},
            expected_schema={"urgency": "string", "category": "string"}
        )
        prompt_a = "Classify: {{query}}"
        prompt_b = "Analyze and classify: {{query}}"
        output_a = '{"urgency": "HIGH", "category": "INFRASTRUCTURE"}'
        output_b = '{"urgency": "CRITICAL", "category": "DEVOPS"}'

        result = self.evaluator.evaluate_case(tc, prompt_a, prompt_b, output_a, output_b)
        self.assertIn(result.verdict, ("PASS", "IMPROVEMENT"))
        self.assertFalse(result.regression_detected)
        self.assertTrue(result.schema_compliance_a)
        self.assertTrue(result.schema_compliance_b)

    def test_evaluate_case_regression(self):
        tc = TestCase(
            id="tc-2",
            name="Strict Schema Adherence",
            description="Must output valid JSON adhering to schema",
            variables={"input": "Customer inquiry"},
            expected_schema={"reply": "string", "action_required": "string"}
        )
        prompt_a = "Provide response as JSON: {{input}}"
        prompt_b = "Be conversational and reply to: {{input}}"

        output_a = '{"reply": "Thank you for contacting us.", "action_required": "false"}'
        # Prompt B regresses to conversational markdown instead of required schema
        output_b = "Sure! Here is what I think: Thank you for reaching out to us today."

        result = self.evaluator.evaluate_case(tc, prompt_a, prompt_b, output_a, output_b)
        self.assertTrue(result.regression_detected)
        self.assertEqual(result.verdict, "REGRESSION")
        self.assertTrue(result.schema_compliance_a)
        self.assertFalse(result.schema_compliance_b)

    def test_evaluate_case_token_inflation(self):
        tc = TestCase(
            id="tc-3",
            name="Brevity Constraint",
            description="Verify token efficiency",
            variables={"text": "Short prompt"},
        )
        prompt_a = "Summarize: {{text}}"
        prompt_b = "You are a very verbose, extremely comprehensive assistant that details every single history: {{text}}"

        output_a = "Brief summary."
        output_b = "Here is an extremely detailed and elaborate breakdown that goes on and on for several paragraphs..." * 5

        result = self.evaluator.evaluate_case(tc, prompt_a, prompt_b, output_a, output_b)
        self.assertGreater(result.token_delta_pct, 40.0)
        self.assertIn(result.verdict, ("WARNING", "REGRESSION"))

    def test_cost_matrix_calculation(self):
        tokens_a = 500  # Baseline tokens per query
        tokens_b = 350  # Candidate prompt optimized to 350 tokens (30% savings)

        matrix = self.evaluator.calculate_cost_matrix(tokens_a, tokens_b, query_volume=1_000_000)

        self.assertIn("gpt-4o", matrix)
        self.assertIn("claude-3-5-sonnet", matrix)
        self.assertIn("gemini-1-5-pro", matrix)

        gpt = matrix["gpt-4o"]
        self.assertEqual(gpt["status"], "SAVINGS")
        self.assertLess(gpt["cost_b_usd"], gpt["cost_a_usd"])
        self.assertLess(gpt["delta_usd"], 0)
        self.assertLess(gpt["delta_pct"], 0)


if __name__ == "__main__":
    unittest.main()
