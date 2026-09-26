---
doc: prd
status: approved
---

# PromptPulse Studio — Product Requirements

Local-first prompt regression, schema validation, and token economy workbench for AI engineers.
Source: `scope.md > The Unique Kernel`.

## The Core Journey
1. **Launch**: Developer opens the live URL or runs the local CLI.
2. **Review Variants**: Developer views the Baseline Prompt (Version A) and Candidate Prompt (Version B).
3. **Customize Scenarios**: Developer inspects preset test cases (JSON Adherence, Edge Injection, Brevity, Complex Context, Extraction) or clicks **"Add Custom Test Case"** to input their own custom parameters.
4. **Run Evaluation**: Developer triggers the evaluation suite; the engine performs instant sub-millisecond evaluation across all scenarios.
5. **Analyze Scorecard**: Developer reviews the regression scorecard showing:
   - **Schema Compliance**: Verified against JSON Schema AST.
   - **Token Delta**: Quantified token count change and projected dollar cost per 1M queries across GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro.
   - **Quality Score**: Heuristic score (0-100) reflecting instruction adherence and safety boundaries.
6. **Export**: Developer clicks **"Export Evaluation Report"** to download `prompt-eval-report.json` or Markdown artifact.

## Screens and Layout
- **Header**: Brand identity (`PromptPulse Studio v1.0`), status indicator ("Local-First Engine Active"), quick actions (Run All, Add Test Case, Export Report).
- **Prompt Comparison Panel (Split View)**:
  - Left Column: Prompt A (Baseline Production Prompt) with token counter and variable chips.
  - Right Column: Prompt B (Candidate Refactor) with token counter, live diff indicator, and variable chips.
- **Model Economy Bar**:
  - Live cost projections comparing Prompt A vs. Prompt B across GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro.
- **Test Case Matrix**:
  - Tabbed or card-based view of test cases.
  - Input variable editor (`{{variable_name}}`).
  - Output side-by-side preview with color-coded diffing.
  - Individual test case status badge (PASS, WARN, REGRESSION).
- **Action Modal / Drawer**:
  - Custom test case creator modal allowing user to define inputs, expected output schema, and constraint flags.

## Look and Feel
- **Theme**: Dark obsidian slate (`#0B0F19`) with high-contrast surfaces (`#1E293B`, `#111827`).
- **Typography**:
  - Display: `Space Grotesk` (clean, contemporary, architectural)
  - UI Text: `Plus Jakarta Sans` (ergonomic, legible)
  - Code & Telemetry: `JetBrains Mono` (tabular numbers and monospace syntax)
- **Accents**:
  - Primary: Electric Indigo (`#4F46E5`)
  - Success/Pass: Emerald (`#10B981`)
  - Warning/Regression: Amber (`#F59E0B`)
  - Danger/Error: Crimson (`#EF4444`)
- **Copy Tone**: Precise, developer-focused, zero fluff, instant feedback.

## Features and Behavior

### 1. Dual Prompt Editor
- Side-by-side editing with synchronized scrolling.
- Automatic extraction and highlighting of mustache template variables (`{{variable}}`).
- Real-time token counter calculation as the user types.

### 2. Multi-Model Token Economy Calculator
- Computes estimated token count (using BPE token approximation: ~4 characters per token).
- Live pricing matrix:
  - OpenAI GPT-4o: $2.50 / 1M input tokens, $10.00 / 1M output tokens
  - Anthropic Claude 3.5 Sonnet: $3.00 / 1M input tokens, $15.00 / 1M output tokens
  - Google Gemini 1.5 Pro: $1.25 / 1M input tokens, $5.00 / 1M output tokens
- Displays exact dollar savings or inflation delta per 1M calls.

### 3. Schema & Constraint Validator
- Validates output structure against expected JSON schemas or regex patterns.
- Verifies key presence, data types, and absence of hallucinated fields.

### 4. Interactive Test Case Runner
- Built-in test cases for immediate evaluation:
  1. Strict JSON Structured Output
  2. Edge Case & Guardrail Prompt Injection Resistance
  3. Concise Financial Metric Summarization
  4. Multi-Condition Routing & Classification
  5. High-Density Document Extraction
- Dynamic User Testing: Allows adding arbitrary custom test cases with custom variables and expectations.

### 5. Report Exporter
- Exports complete deterministic evaluation payload including prompt versions, test case outputs, diffs, and benchmark scores in JSON and Markdown formats.

## States and Boundaries
- **Initial State**: Populated with realistic production prompt templates (Customer Support Agent with JSON output) and 5 pre-configured test scenarios.
- **Editing State**: Real-time token updates and variable chip refresh.
- **Evaluation State**: Instant execution with visual pass/fail indicator animations.
- **Custom Test State**: User can add, edit, or delete custom test cases; changes persist in browser `localStorage`.

## Non-Goals
- Calling external paid APIs directly from the client without user opt-in (must work 100% offline out-of-the-box).
- Complex academic math or LaTeX equation dumps (focus purely on clear developer metrics: tokens, cost, schema validity).
- Disposable hackathon UI or references to the competition.
