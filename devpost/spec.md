---
doc: spec
status: approved
---

# PromptPulse Studio — Technical Spec

## How This Works, In Plain Language
PromptPulse Studio operates as a local-first client-side evaluation engine and companion Python CLI.
1. The user inputs two prompt templates: Baseline (Prompt A) and Candidate (Prompt B).
2. The template engine parses template variables in `{{variable}}` syntax.
3. Test case values are substituted into the prompt templates.
4. The local evaluation engine analyzes the prompt and simulated responses for:
   - Output schema compliance (parsing JSON and validating expected keys).
   - Token efficiency (calculating prompt and completion tokens).
   - Token cost across three major LLM providers (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro).
   - Regression delta (scoring structural variance, verbosity drift, and schema breakage).
5. Results are visually presented in a split-screen dashboard and exportable as JSON/Markdown reports.

## The Core Journey Through the System
1. User enters or modifies Prompt A / B in the UI (`web/app.js`).
2. Event listeners trigger `calculateTokens()` and `extractVariables()`.
3. User triggers "Run Evaluation Suite" → `evaluateAllCases()` executes synchronously.
4. Heuristic evaluators compute individual test scores and aggregated regression index.
5. DOM updates with color-coded diffing, model cost comparison tables, and badge statuses.
6. User clicks "Export Report" → creates a downloadable JSON blob.

## Stack
- **Frontend**: Pure Semantic HTML5, CSS3 with modern CSS variables, and Vanilla JavaScript (ES2022). Zero build-step overhead, zero node_modules required for the web client, sub-millisecond execution.
- **Backend / CLI Engine**: Python 3.10+ with `pydantic` and `pytest` for deterministic testing.
- **Deployment**: Vercel Edge Network (static hosting with instant edge caching).
- **Fonts**: Google Fonts (`Space Grotesk`, `Plus Jakarta Sans`, `JetBrains Mono`).

## Where It Runs and How Someone Tries It
- **Live Edge Deployment**: Accessible on Vercel at `https://promptpulse-studio.vercel.app` (or generated Vercel alias).
- **Local Testing**:
  - Open `web/index.html` in any browser.
  - Or run Python CLI: `python3 cli/promptpulse.py --run-eval`
  - Or run test suite: `pytest engine/test_engine.py -v`

## Look and Feel
- Background: `#0B0F19` (Obsidian Slate)
- Card Surfaces: `#131B2E` with `1px solid rgba(255, 255, 255, 0.08)`
- Primary Accent: `#4F46E5` (Electric Indigo)
- Success Indicator: `#10B981` (Emerald)
- Warning/Regression: `#F59E0B` (Amber)
- Code Font: `'JetBrains Mono', monospace`
- UI Font: `'Plus Jakarta Sans', sans-serif`
- Title Font: `'Space Grotesk', sans-serif`

## Components
1. `PromptEditor`: Dual textareas with synced line numbering, token telemetry, and extracted variable pills.
2. `TokenEconomyBar`: Cost comparison table showing price per 1M calls for GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro.
3. `TestCaseMatrix`: Interactive card grid displaying individual test case inputs, Prompt A output, Prompt B output, and diff highlights.
4. `CustomTestCaseModal`: Interactive form to add custom scenarios with dynamic variables and expected outputs.
5. `ReportExporter`: Client-side JSON & Markdown report generator.
6. `CLI Runner`: Terminal tool parsing prompts from files and generating stdout regression matrices.

## File Structure
```
promptpulse/
├── devpost/
│   ├── learner-profile.md
│   ├── scope.md
│   ├── prd.md
│   ├── spec.md
│   └── checklist.md
├── engine/
│   ├── __init__.py
│   ├── evaluator.py
│   └── test_engine.py
├── web/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── cli/
│   └── promptpulse.py
├── demo/
│   ├── promptpulse_demo.mp4
│   └── voiceover_script.txt
├── submission/
│   ├── devpost_submission.md
│   ├── AI_DISCLOSURE.md
│   └── LICENSE
├── assets/
│   ├── logo.png
│   └── banner.png
├── vercel.json
└── README.md
```

## External Services and Dependencies
- **CDN**: Google Fonts (`Space Grotesk`, `Plus Jakarta Sans`, `JetBrains Mono`).
- **Dependencies**: Zero external runtime NPM dependencies; 100% self-contained client-side web application.
- **Python**: Standard library (`json`, `re`, `argparse`, `sys`, `typing`) + `pytest` for automated testing.

## Important Failure Modes
1. **Invalid JSON Schema in Test Case**: If a user enters an invalid JSON string as expected schema, the editor displays an inline syntax warning without crashing.
2. **Missing Template Variable**: If a test case omits a variable defined in `{{var}}`, the engine highlights the unpopulated token in amber and runs with an empty default value.
3. **Severe Token Inflation (> 50%)**: If Prompt B exceeds Prompt A by over 50% in token volume, an alert badge is displayed with cost warning.

## What Was Simplified and Why
- **Local Heuristic Evaluation instead of Live OpenAI API Keys**: Allows anyone (including judges and developers without paid API accounts) to test all features instantly, deterministically, and with zero cost or network latency.
- **BPE Character Approximation**: Uses industry-standard 4 chars/token heuristic for instant client-side calculation rather than loading a 50MB WASM tokenizer.
