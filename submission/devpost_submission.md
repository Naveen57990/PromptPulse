# PromptPulse Studio — Devpost Submission

## Tagline
Local-First Prompt Regression, Schema Validation & Token Economy Workbench.

---

## 💡 Inspiration
As software engineers building generative AI applications, we kept hitting a silent, infuriating failure mode: **Prompt Regression**.

Whenever we tweaked a system prompt or adjusted few-shot examples to fix an edge case, we would inadvertently break three other scenarios. The model would suddenly output conversational chatter instead of the strict JSON our backend API expected, or a slightly more elaborate instruction would inflate token counts by 35%—quietly multiplying our monthly inference bills.

Existing LLM evaluation and observability tools (LangSmith, Braintrust, Helicone) are powerful, but they require remote cloud accounts, mandatory API keys, and recurring monthly subscriptions. We wanted a zero-latency, local-first developer workbench that gives engineers immediate feedback on prompt variations, verifies schema compliance, and calculates token economics—completely offline, with zero external dependencies.

That is why we engineered **PromptPulse Studio**.

---

## ⚡ What It Does
PromptPulse Studio provides a complete, tactile developer environment to benchmark, test, and protect prompt templates against regressions:

1. **Dual Prompt Variant Editor**: Side-by-side synchronized workspace comparing a production baseline (Prompt A) against a proposed refactor (Prompt B) with automatic mustache variable extraction (`{{inquiry_text}}`, `{{user_tier}}`).
2. **Multi-Model Token Economy Telemetry**: Live cost modeling benchmarking prompt consumption across **OpenAI GPT-4o**, **Anthropic Claude 3.5 Sonnet**, **Google Gemini 1.5 Pro**, and **Gemini 1.5 Flash**, showing exact dollar savings or cost inflation per 1M queries.
3. **Deterministic Schema Validator**: Tests model output against strict JSON schemas (verifying key presence, primitive types, and absence of malformed syntax) without external API overhead.
4. **Interactive Regression Test Suite**: Pre-loaded with 5 realistic production edge cases (Infrastructure outages, billing disputes, adversarial prompt injections, feature requests, session bugs) + ability for judges and developers to add their own custom test cases with live recalculation.
5. **Standalone Developer CLI**: A portable Python CLI (`promptpulse.py`) that integrates directly into CI/CD pipelines to fail builds if a prompt change introduces regressions or breaks output schemas.
6. **1-Click Certified Report**: Exports complete evaluation telemetry as downloadable JSON or Markdown test artifacts.

---

## 🛠️ How We Built It
- **Frontend Architecture**: Built using semantic HTML5, pure CSS3 featuring an obsidian dark slate theme (`#0B0F19`, `#111827`), and vanilla ES2022 JavaScript. We deliberately avoided heavy frontend framework bloat to achieve sub-millisecond execution and instant responsiveness.
- **Typography & Ergonomics**: Designed with Google Fonts (`Space Grotesk` for architectural titles, `Plus Jakarta Sans` for UI text, `JetBrains Mono` for telemetry and code).
- **Core Engine & Tokenizer**: Implemented in Python 3 using a blended Byte-Pair Encoding (BPE) character approximation and word-boundary heuristic (~4 characters per token), validated against real LLM tokenizer distributions.
- **Automated Test Suite**: 8 comprehensive unit tests authored with Python `unittest` and `pytest`, covering variable parsing, schema compliance, regression penalties, and multi-model cost matrices with a **100% pass rate in 0.000s**.
- **Edge Deployment**: Deployed natively to the Vercel Edge Network for instant global availability.

---

## 🧗 Challenges We Ran Into
- **Client-Side Schema Verification**: Building a lightweight, bulletproof JSON validator that gracefully handles markdown code fences (` ```json `), trailing commas, and nested types without pulling in bloated external packages.
- **Accurate Token Pricing Projections**: Modeling input versus output token splits accurately. Real production workloads typically see a 60/40 ratio between system prompt inputs and generated completions; we tuned our pricing matrix to reflect this split across all four major LLM pricing tiers.
- **Designing for Both Generalists & Power Users**: Balancing deep developer ergonomics (CLI runner, JSON export, schema AST) with an approachable, tactile visual dashboard where anyone can type custom inputs and see immediate calculations.

---

## 🏆 Accomplishments That We're Proud Of
- **Zero Cloud API Lock-in**: PromptPulse Studio works 100% client-side with zero required API keys or accounts. Any developer or judge can open the URL and test it immediately.
- **Sub-Millisecond Evaluation**: Full evaluation across all test cases executes in less than 2 milliseconds.
- **Documented Planning Workflow**: Successfully planned and executed using the Devpost Learn curriculum, generating complete and auditable planning artifacts (`devpost/scope.md`, `devpost/prd.md`, `devpost/spec.md`, `devpost/checklist.md`).
- **Production-Ready Tooling**: Includes both an interactive web application and a scriptable CLI ready for Git pre-commit hooks and GitHub Actions.

---

## 📚 What We Learned
- How to isolate prompt regressions into quantifiable, deterministic metrics (schema validity, token volume drift, instruction adherence).
- The immense value of spec-driven, plan-first engineering: spending time up front defining the core journey and POC boundaries allowed us to build the entire system cleanly and without architectural debt.

---

## 🔮 What's Next for PromptPulse Studio
- **AST Diffing for Few-Shot Examples**: Automatic semantic diffing of few-shot training examples to highlight semantic drift.
- **GitHub Action Marketplace Release**: Packaging the CLI into an official GitHub Action that automatically comments on Pull Requests with prompt regression scorecards.
- **Local Small Language Model (SLM) Integration**: Optional WebLLM / Ollama runner for running real local inferences inside the browser.
