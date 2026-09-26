---
doc: scope
status: approved
---

# PromptPulse Studio

Local-first prompt regression, schema validation, and token economy workbench for AI engineers.

## The Unique Kernel
Deterministic side-by-side prompt regression testing that detects breaking changes in output structure, JSON schema compliance, and token inflation *before* updates hit production, running entirely client-side with zero required API keys.

## Who It's For
AI application developers and prompt engineers who repeatedly edit system instructions and few-shot examples, currently relying on manual eyeballing or unpredictable production monitoring.

## The Core Loop
1. Open PromptPulse Studio.
2. View baseline Prompt A vs. candidate Prompt B with live syntax diffing.
3. Run or customize test cases with dynamic variables (`{{user_query}}`, `{{context}}`).
4. Review the instant regression scorecard: Schema Integrity (Pass/Fail), Token Delta (%), Cost Projection ($), and Output Consistency.
5. Export a certified `prompt-eval-report.json` or Markdown summary for pull request reviews.

## Inspiration & Identity
- **Inspiration**: Raycast, Vitest UI, Postman, Linear.
- **Aesthetic**: Deep obsidian slate (`#0B0F19`), electric indigo accents (`#4F46E5`), emerald compliance badges (`#10B981`), amber regression alerts (`#F59E0B`).
- **Typography**: Space Grotesk for architectural titles, Plus Jakarta Sans for interface typography, JetBrains Mono for code blocks and token telemetry.

## Why This Matters to the Learner
Prompt engineering without regression testing is like pushing code without unit tests. Every developer building AI applications needs an instantaneous local safety net.

## What "Working" Looks Like
A fully interactive web application where a user can modify prompts, click "Add Custom Test Case", input custom test variables, run evaluations, observe real-time diffing and token cost calculations across GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro, and export the test report.

## The POC Boundary
- **In Scope**:
  - Dual prompt variant editor (Prompt A vs. Prompt B) with variable detection.
  - Interactive test case runner with 5 built-in edge scenarios + custom user scenario builder.
  - Local deterministic heuristic evaluation engine (schema validity, token cost calculation, latency benchmark, regression score).
  - Multi-model token cost calculator (OpenAI, Anthropic, Google Gemini).
  - Standalone runnable CLI tool (`promptpulse.py`) with 100% automated pytest coverage.
  - 1-click JSON/Markdown evaluation report exporter.
- **Deferred / Later**:
  - Remote cloud team collaboration sync.
  - Multi-turn conversational session history replay.
  - Automated genetic prompt optimization search.

## Explicitly Cut
- Cloud authentication & paywalled subscription tiers (must remain 100% free, local-first, and open source).
- Live remote API token billing integration (evaluation works deterministically without paying third parties).
