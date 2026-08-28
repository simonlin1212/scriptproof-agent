# ScriptProof project rules

ScriptProof is a new submission for the Agentic Cinema hackathon, Parallel track. The submission deadline is **2026-09-10 05:00 Asia/Singapore**.

## Read first

1. `NEXT.md` for current status and the next safe action.
2. `DEV_LOG.md` for implementation decisions and evidence.
3. `docs/COMPETITION_RULES.md` before changing the stack or submission scope.

## Competition gates

- This must remain a new, independent project. Do not turn Agentic Brief into this product or copy its repository history.
- AI and agent tooling may use only Google Cloud AI plus Parallel's allowed capabilities. Do not add OpenAI, Anthropic, AWS AI, or another agent framework.
- The production path must call Parallel Search at runtime. A README mention, mock, or cached result does not satisfy the track requirement.
- The product must use Gemini and Google ADK / Agent Builder.
- Final delivery requires a hosted app, public open-source repository, English project description, and a public demo video no longer than three minutes.

## Product contract

- Target users are screenwriters and pre-production teams.
- The core flow is: read screenplay → identify research claims → call Parallel → preserve citations → check continuity → produce revision actions.
- Supported and contradicted findings require at least one working HTTPS source.
- Uncertain evidence stays uncertain. Never fabricate, repair, or silently replace citations.
- Production has no fake-data fallback. Test doubles are allowed only in tests and visual QA.

## Engineering constraints

- Python 3.12, Google ADK, Gemini 3.5 Flash, Flask, Parallel's official `parallel-google-adk` package.
- Vertex AI location is `global`.
- Secrets stay in `.env` locally and Secret Manager in production. Never commit them.
- Keep the paid analysis endpoint bounded and optionally protected by `SCRIPT_PROOF_ACCESS_CODE`.
- All changes must pass Ruff, pytest, 80%+ coverage, interface QA, and an independent pre-push review.
