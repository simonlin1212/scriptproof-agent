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

### Google Cloud credit request

The official Agentic Cinema Google Cloud credit form was submitted successfully on 2026-08-28 for `linsizhen@gmail.com`, Devpost username `linsizhen`, country `Hong Kong`, and partner integration `Parallel Search API`. The form states that approved credits should arrive within five business days and that the coupon must be redeemed by August 31, 2026 at 11:59 PM PST.

## 2026-08-28 — Live integration accepted

Simon supplied the Parallel credential. It was stored only in the repository's
ignored `.env` file with mode `600`; the credential was not committed or copied
into documentation.

The sample screenplay completed repeatedly against real Gemini 3.5 Flash on
Vertex AI and the official Parallel ADK tools. The first reviewable run produced
six Parallel calls, two findings, and six citations. Manual inspection found two
weak publisher types, so the researcher instructions were tightened to prefer
identifiable institutional and established sources and to return `uncertain`
when only weak evidence is available.

The improved run returned citations from the University of Illinois preservation
program, IEEE Spectrum, the National Inventors Hall of Fame, and RTÉ Archives.
The final bounded smoke test completed successfully with five Parallel calls and
citations from DePaul University, Computer History Museum, IEEE Spectrum, and an
established technical reference.

An independent review identified an unbounded retry/cost risk in the stronger
source-search instruction. The fix caps research at two searches and one fetch
per claim and passes an ADK `RunConfig` limiting the complete workflow to 20 LLM
calls. Final verification: Ruff clean, 38 tests passed, 86.79% coverage, bounded
live smoke passed, and the follow-up independent review found no actionable
regressions.

## 2026-08-28 — Production deployment and source-quality gate

ScriptProof was deployed to Cloud Run in `asia-southeast1` using the dedicated
`scriptproof-runtime` service account. Gemini remains pinned to the Vertex AI
`global` model location. The Parallel key and reviewer code are read from Secret
Manager, the request timeout is 600 seconds, and the judging deployment is
bounded to one instance.

The deployed service passed four production checks: health returned HTTP 200,
an anonymous paid API request returned HTTP 403, the sample screenplay completed
against real Gemini 3.5 Flash and Parallel, and the public report preserved only
URLs observed in successful Parallel responses. The accepted cloud run made six
Parallel calls, produced two research findings, scored the draft 85/100, and
preserved six citations from institutional or established publishers.

Prompt guidance alone was not treated as a sufficient quality control. A
deterministic post-research gate now removes blocked low-authority publisher
classes before the editor sees them. If removing those sources leaves a
definitive verdict without evidence, the verdict is downgraded to `uncertain`.
A final validation gate also rejects any report that reintroduces a blocked
citation.

The Story Editor now receives only controlled structured state plus sanitized,
length-bounded production context. It does not inherit the raw prior-agent
conversation. User context is treated as untrusted data, delimiter-like input is
escaped, and the editor has no research tools.

Regression work covered hostname normalization, lookalike domains, source
removal, verdict downgrades, state sanitization, current-turn isolation, context
preservation, and delimiter injection. Final engineering verification: Ruff
clean, 47 tests passed, 89.00% coverage, full-history secret scan clean, and an
independent review found no actionable regressions.

Browser QA used the successful production report as a deterministic visual test
fixture. All 16 assertions passed on desktop and a 390-pixel mobile viewport,
including form completion, HTTPS citations, blocked-source absence, runtime
evidence display, and horizontal-overflow checks. Both screenshots were also
inspected visually.

## 2026-08-28 — Public repository and demo

The repository was published at `https://github.com/simonlin1212/scriptproof-agent`.
The first public GitHub Actions run installed the locked environment, passed
Ruff, and passed the full test suite. Repository metadata points to the hosted
Cloud Run service.

The English demo was built from reviewed 1920×1080 browser captures of the live
interface and the accepted real-run report. It includes the input flow, research
state, evidence ledger, continuity desk, production handoff, architecture, and
runtime counters. The narration was transcribed after synthesis to check for
missing lines, normalized to -16 LUFS, and delivered with burned-in English
captions.

The final H.264/AAC video is 1920×1080, 30 fps, `yuv420p`, and 2:17 long. It was
published publicly at `https://youtu.be/hyHVu464XAM`; an anonymous metadata check
confirmed the title, duration, public availability, and watch URL.

## 2026-08-29 — Credential rotation and Devpost registration

Production was first pinned to the last known-good Parallel secret version so a
change to `latest` could not affect the live service unexpectedly. A new secret
version was then deployed to a tagged, zero-traffic Cloud Run revision. Its
health check returned HTTP 200, an anonymous paid request returned HTTP 403, and
a complete sample analysis returned HTTP 200 with real Gemini and Parallel
calls before traffic moved.

During the rotation audit, that candidate credential appeared once in private
operator output. It was treated as exposed instead of being accepted. A second
new Parallel key and Secret Manager version were created and put through the
same zero-traffic process. The final candidate completed three Parallel calls,
two findings, two accepted citations, and zero blocked source domains. Cloud Run
revision `scriptproof-web-00007-der` then received 100% of production traffic.

The original key and the discarded candidate key were deleted from Parallel.
Secret Manager versions 1, 2, and 3 are disabled; production is pinned to enabled
version 4. Temporary Cloud Run traffic tags were removed. The public health
check still returns HTTP 200 after the old versions were disabled.

The Agentic Cinema registration form was submitted successfully. The project is
registered as a solo entry with marketing opt-in left off. Devpost requires an
interactive reCAPTCHA before the project record itself can be created, so the
final submission resumes immediately after that manual gate is completed.
