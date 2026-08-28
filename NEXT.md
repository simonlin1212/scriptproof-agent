# ScriptProof current status

> Current phase: **hosted app, public repository, public demo, and Devpost registration complete; final submission in progress.**
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
- Public GitHub repository created and CI passed on `main`.
- Public English demo published to YouTube at 2:17, below the 3-minute limit;
  anonymous metadata verification confirms `public` availability.
- English Devpost copy, architecture graphic, reviewed screenshots, narration,
  and subtitle source are complete.
- Parallel production credentials were rotated through two zero-traffic
  candidates. The accepted revision is pinned to Secret Manager version 4;
  versions 1-3 are disabled and the obsolete Parallel API keys were deleted.
- Devpost registration is complete with Hong Kong as the account region.
- Agentic Brief parent repository remains clean.

## Next actions

1. Complete the Devpost human-verification gate, create the project, select the
   Parallel track, provide the reviewer
   access code in the private judging instructions, and submit.
2. Verify the entry status and all public links from the submitted project page.

## Current blocker

No engineering blocker. Devpost currently requires a manual reCAPTCHA before it
will create the project; the submission package itself is complete.
