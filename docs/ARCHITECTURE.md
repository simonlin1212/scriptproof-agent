# ScriptProof architecture

## Product boundary

ScriptProof is a single-purpose pre-production agent. It accepts plain screenplay text and optional production context, then returns a structured report. It does not edit files, contact people, publish material, or make legal or safety decisions.

## Agent sequence

### Script Analyst

- Reads the screenplay without web tools.
- Produces at most five externally verifiable claims.
- Identifies continuity candidates and production questions.
- Uses `ScriptAnalysis` as a strict output contract.

### Evidence Researcher

- Receives the structured analysis through ADK session state.
- Calls Parallel `web_search` for every selected claim.
- May call `web_fetch` when a source needs full-page context.
- Prefers first-party and institutional evidence.
- Uses `ResearchBundle` as a strict output contract.

### Story Editor

- Receives both prior structured records.
- Cannot call search tools or introduce new sources.
- Converts evidence and continuity candidates into department actions.
- Uses `ScriptReport` as the public output contract.

## Runtime path

```text
Browser
  |
  | POST /analyze (bounded screenplay + optional reviewer code)
  v
Flask / Cloud Run
  |
  | Google ADK Runner
  v
Gemini Script Analyst
  |
  v
Gemini Evidence Researcher ---- Parallel Search API
  |                                  |
  |<------ excerpts + citations -----+
  v
Gemini Story Editor
  |
  | Pydantic validation + Jinja auto-escape
  v
Evidence ledger + continuity desk + production handoff
```

## Trust boundaries

- Screenplay input is untrusted and normalized before model use.
- Model output is untrusted until Pydantic validation succeeds.
- Source URLs are accepted only when they are valid HTTPS URLs.
- Provider exceptions are logged server-side; the client receives a generic error.
- Secrets come from local environment variables or Secret Manager, never source code.
- The optional reviewer code protects the paid endpoint with constant-time comparison.

## Failure semantics

- Invalid or short screenplay: HTTP 400 with a specific corrective message.
- Missing or incorrect reviewer code: HTTP 403.
- Oversized request: HTTP 413.
- Google, Parallel, parsing, or orchestration failure: HTTP 500 with a generic message.
- No fake report is returned on provider failure.

## Current trade-offs

- Analysis is synchronous to keep the first submission small and auditable. Cloud Run uses a 600-second timeout.
- Reports are not persisted in the MVP. The next production increment can add Firestore without changing the agent contracts.
- Plain text is accepted first. PDF parsing is intentionally deferred so the demo centers on agent behavior rather than file-format handling.
