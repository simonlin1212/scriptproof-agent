# ScriptProof current status

> Current phase: **production deployment and browser QA complete; preparing the public submission package.**
>
> Deadline: 2026-09-10 05:00 Asia/Singapore.

## Completed

- Independent project and Git repository created.
- Official competition and SDK research completed.
- Script Analyst → Evidence Researcher → Story Editor pipeline implemented with Google ADK.
- Parallel official tools wired into the production agent.
- Structured report contracts, web app, API, Dockerfile, sample scene, and competition documentation completed.
- 47 tests passing with 89.00% coverage.
- Ruff clean.
- Independent review completed; all five findings fixed with regression tests.
- Final pre-push review found no actionable regressions.
- Official $100 Google Cloud credit request submitted on 2026-08-28; confirmation received.
- Parallel API key configured locally in the ignored, mode-600 `.env` file.
- Multiple live Gemini 3.5 + Parallel runs completed successfully.
- Final bounded smoke test completed with five Parallel calls, two findings, and
  citations from established technical and institutional publishers.
- Research instructions now reject weak publisher classes and cap search attempts.
- ADK execution is capped at 20 LLM calls per report to bound cost and runtime.
- Current verification: Ruff clean, 47 tests passing, 89.00% coverage, and final
  independent review found no actionable regressions.
- Deployed to Cloud Run as `scriptproof-web` with a dedicated runtime identity,
  Secret Manager integration, a 600-second timeout, and one-instance cost bound.
- Production health check, anonymous paid-endpoint rejection, and a real cloud
  Gemini + Parallel analysis all passed.
- The production run completed with six Parallel calls, two findings, six
  preserved citations, and zero blocked low-authority sources.
- Deterministic source-quality filtering and Story Editor context isolation are
  enforced after model output, not only requested in prompts.
- Desktop and 390-pixel mobile browser QA passed all 16 functional assertions;
  the live report has no horizontal overflow.
- Agentic Brief parent repository remains clean.

## Next actions

1. Rotate the pre-release Parallel credential with a staged rollout: first pin
   production to its current secret version, then add the new version, deploy a
   tagged no-traffic candidate pinned to it, validate the candidate, shift
   traffic, and only then revoke the old credential.
2. Create the public GitHub repository.
3. Produce the English Devpost page, architecture graphic, screenshots, and
   ≤3-minute public demo.
4. Submit to the Parallel track and verify `SUBMITTED` before the deadline.

## Current blocker

No engineering blocker. One manual account-security gate and the submission
packaging remain.
