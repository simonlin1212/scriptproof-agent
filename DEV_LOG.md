# ScriptProof development log

## 2026-08-28 — Project created

### Direction

Simon approved a new Agentic Cinema entry focused on screenplay research and continuity checking. The project was created inside the Agentic Brief directory as an independent nested Git repository. The parent repository excludes it through local `.git/info/exclude`, so the already-submitted Agentic Brief snapshot remains clean.

### Research before implementation

Official and open-source sources were checked before coding:

- Agentic Cinema overview, rules, resources, and five partner pages.
- Parallel's official `parallel-google-adk` package and example agent.
- Parallel Python SDK, cookbook, Gemini grounding example, and PyPI releases.
- Google ADK structured-output and sequential-state examples.
- GitHub searches for screenplay research agents and existing product names.

Decision: adopt `parallel-google-adk==0.0.1` instead of writing a custom Parallel wrapper. It directly satisfies the track's runtime integration requirement and provides citations plus tool-call tracing.

### Product architecture

Product name: **ScriptProof**.

Three-stage workflow:

1. Script Analyst creates a bounded structured research plan.
2. Evidence Researcher calls Parallel Search and returns cited verdicts.
3. Story Editor produces the evidence ledger, continuity desk, and production handoff.

The web surface is Flask and server-rendered Jinja. Pydantic contracts sit between every agent and the interface. The design direction is editorial screenplay paper, red pencil proofing, and dark production workspace.

### Test-first implementation

The initial tests were written before the modules and failed at import as expected. After implementation:

- Ruff: passed.
- pytest: 37 passed.
- coverage: 86.71%.
- desktop browser QA: no horizontal overflow.
- homepage and report preview: visually inspected.
- parent Agentic Brief Git repository: clean.

### Security and cost controls

- Bounded and normalized screenplay input.
- HTTPS-only citations.
- Every public citation must exactly match a URL observed in a Parallel tool response.
- Research claims cannot produce a successful report without a completed Parallel call.
- Dotenv loading is pinned to this repository and cannot inherit a parent project's secrets.
- Pydantic validation of all public model output.
- Jinja auto-escaping; model text is never marked safe.
- Generic provider errors.
- Optional constant-time reviewer access code for paid analysis calls.
- Secrets excluded from Git and intended for Secret Manager.

### Independent review

The first local Codex review found five actionable issues: parent dotenv inheritance, missing Parallel call enforcement, missing citation provenance enforcement, non-object API payload failures, and noncanonical Vertex locations. A second review found that a failed `web_fetch` fallback could echo an unverified URL; this was also fixed test-first. The documented local server now bypasses Flask CLI's parent dotenv search. The final review found no actionable regressions. Ruff, 37 tests, 86.71% coverage, dependency audit, package build, local server smoke test, and secret scan all passed.

### Known external blocker

Google Application Default Credentials are available and the existing GCP project is reachable. No `PARALLEL_API_KEY` was found in the environment or project configuration. A Parallel account/key is required before the first real end-to-end research run.
