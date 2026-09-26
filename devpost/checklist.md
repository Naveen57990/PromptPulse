---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. Dual Prompt Editor & Live Variable Extraction**
  Becomes usable: Interactive side-by-side prompt editor showing real-time token counts and extracted `{{variable}}` pills.
  PRD ref: `prd.md > Features and Behavior > 1. Dual Prompt Editor`
  Spec ref: `spec.md > Components > PromptEditor`
  Build: Construct HTML/CSS layout with split-screen textareas and JS event listeners extracting template variables.
  Verify (mechanical): Type template with `{{user_name}}` and confirm pill renders; verify token counter recalculates.
  Commit: `Add dual prompt editor and variable parser`

- [x] **2. Multi-Model Token Economy Calculator**
  Becomes usable: Live comparison table showing cost per 1M calls across GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro.
  PRD ref: `prd.md > Features and Behavior > 2. Multi-Model Token Economy Calculator`
  Spec ref: `spec.md > Components > TokenEconomyBar`
  Build: Implement token pricing math and render savings/inflation delta indicators.
  Verify (mechanical): Confirm cost updates dynamically on prompt modification.
  Commit: `Implement multi-model token economy engine`

- [x] **3. Deterministic Evaluation Engine & Test Case Matrix**
  Becomes usable: Running 5 pre-configured edge test scenarios through local schema and regression validators.
  PRD ref: `prd.md > Features and Behavior > 3. Schema & Constraint Validator`
  Spec ref: `spec.md > Components > TestCaseMatrix`
  Build: Add test case cards, execution handler, JSON schema checker, and color-coded diffing.
  Verify (mechanical): Click "Run Evaluation Suite" and verify all 5 test cases compute passes/warnings.
  Commit: `Add evaluation engine and test case matrix`

- [x] **4. Custom Scenario Builder & JSON Exporter**
  Becomes usable: Modal dialog allowing user to add custom test cases and download certified evaluation report.
  PRD ref: `prd.md > Features and Behavior > 4. Interactive Test Case Runner`, `5. Report Exporter`
  Spec ref: `spec.md > Components > CustomTestCaseModal`, `ReportExporter`
  Build: Modal dialog with variable input fields, localStorage persistence, and JSON file download trigger.
  Verify (mechanical): Create custom test case, verify it runs and is included in the exported JSON report.
  Commit: `Add custom test case builder and report exporter`

- [x] **5. Standalone Python CLI & Pytest Verification Suite**
  Becomes usable: Automated pytest assertions for CI/CD terminal pipelines.
  PRD ref: `prd.md > Features and Behavior`
  Spec ref: `spec.md > Components > CLI Runner`
  Build: Write `evaluator.py`, `test_engine.py`, and `promptpulse.py`.
  Verify (mechanical): Run `pytest engine/test_engine.py` and verify 100% pass rate.
  Commit: `Add Python CLI and automated pytest suite`

## Hands-on Checkpoints
- [x] Early usable behavior explored — verified dual prompt editor and variable token extraction.
- [x] Final kick-the-tires exploration and feedback completed — verified live edge deployment on Vercel and custom test case creator.

## Final Review
- [x] Final review complete — 100% test pass rate, live edge deployment active, demo video recorded.

## Code Tour and App Map
- [x] Learning activity complete — verified end-to-end prompt regression workflow.
- [x] `devpost/checklist.md` completed with all slices validated.

## Revisions
- (None. Build proceeded exactly according to spec.)
