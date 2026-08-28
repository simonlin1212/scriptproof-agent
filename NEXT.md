# ScriptProof current status

> Current phase: **submitted to Devpost. Public entry and production service are live.**
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
- Devpost entry submitted to the Parallel track at
  `https://devpost.com/software/scriptproof`; the management page shows
  `SUBMITTED` and `5/5 steps done`.
- The submitted public page contains the hosted app, public repository, public
  English demo, MIT-licensed source, eight technology tags, and six media images.
- The reviewer access code is present only in Devpost's private judge information.
- Agentic Brief parent repository remains clean.

## Next actions

1. Keep the Cloud Run service healthy through judging.
2. Preserve the submitted repository, video, and Devpost materials. Make changes
   only for a verified availability, security, or eligibility problem, followed
   by full revalidation.

## Current blocker

No blocker. The entry is submitted.
