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
- 24 tests passing with 88% coverage.
- Ruff clean.
- Homepage and report visual QA passed.
- Agentic Brief parent repository remains clean.

## Next actions

1. Obtain a Parallel API key from `https://platform.parallel.ai/`.
2. Put the key only in local `.env` and run the sample screenplay against real Gemini + Parallel.
3. Inspect every citation and agent verdict; adjust prompts or schemas if necessary.
4. Run the independent code and security review, fix findings, and rerun the full suite.
5. Deploy to Cloud Run with Secret Manager and a reviewer access code.
6. Perform live browser and failure-path QA.
7. Create the public GitHub repository only after the pre-push review is clean.
8. Produce the English Devpost page, architecture graphic, screenshots, and ≤3-minute public demo.
9. Submit to the Parallel track and verify `SUBMITTED` before the deadline.

## Current blocker

`PARALLEL_API_KEY` is not configured. Do not add a fake production fallback; the live call is part of the competition requirement.
