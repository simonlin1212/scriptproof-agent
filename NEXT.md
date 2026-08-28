# ScriptProof current status

> Current phase: **local MVP implemented and verified; live Parallel integration not yet run.**
>
> Deadline: 2026-09-10 05:00 Asia/Singapore.

## Completed

- Independent project and Git repository created.
- Official competition and SDK research completed.
- Script Analyst → Evidence Researcher → Story Editor pipeline implemented with Google ADK.
- Parallel official tools wired into the production agent.
- Structured report contracts, web app, API, Dockerfile, sample scene, and competition documentation completed.
- 37 tests passing with 86.71% coverage.
- Ruff clean.
- Independent review completed; all five findings fixed with regression tests.
- Final pre-push review found no actionable regressions.
- Homepage and report visual QA passed.
- Agentic Brief parent repository remains clean.

## Next actions

1. Obtain a Parallel API key from `https://platform.parallel.ai/`.
2. Put the key only in local `.env` and run the sample screenplay against real Gemini + Parallel.
3. Inspect every citation and agent verdict; adjust prompts or schemas if necessary.
4. Deploy to Cloud Run with Secret Manager and a reviewer access code.
5. Perform live browser and failure-path QA.
6. Create the public GitHub repository.
7. Produce the English Devpost page, architecture graphic, screenshots, and ≤3-minute public demo.
8. Submit to the Parallel track and verify `SUBMITTED` before the deadline.

## Current blocker

`PARALLEL_API_KEY` is not configured. Do not add a fake production fallback; the live call is part of the competition requirement.
