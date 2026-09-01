<p align="center"><b>English</b> | <a href="README_zh.md">简体中文</a></p>

<h1 align="center">ScriptProof</h1>

<p align="center">
  <b>Research before the first take.</b><br>
  Screenplay research · Evidence ledger · Continuity review · Production handoff
</p>

<p align="center">
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-171714">
  <img alt="Google ADK" src="https://img.shields.io/badge/Google_ADK-2.8-B52B22">
  <img alt="Gemini" src="https://img.shields.io/badge/Gemini-3.5_Flash-171714">
  <img alt="Parallel" src="https://img.shields.io/badge/Parallel-Search_API-B52B22">
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-171714">
</p>

<p align="center">
  <a href="#what-it-does">What it does</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#run-locally">Run locally</a> ·
  <a href="#testing">Testing</a> ·
  <a href="docs/COMPETITION_RULES.md">Competition gates</a>
</p>

---

## The Author Is Open to Opportunities

The author is open to AI roles at Tencent and other leading technology companies in Shenzhen, and hopes to join a team passionate about AI development. Areas of interest include AI / Agent product development, real-world deployment, and AI consulting.

Contact: [simonlin0423@gmail.com](mailto:simonlin0423@gmail.com)

---
![ScriptProof interface](docs/assets/scriptproof-home.png)

## What it does

ScriptProof turns a screenplay draft into a cited pre-production brief. It is not a general chatbot and it does not rewrite the story by default.

1. A **Script Analyst** reads the draft and isolates the small number of external claims that could break period accuracy, safety, legal credibility, location realism, or technology.
2. An **Evidence Researcher** calls Parallel Search at runtime, prefers primary and institutional sources, and returns claim-level verdicts with preserved URLs.
3. A **Story Editor** combines the evidence with cross-scene continuity analysis and produces concrete actions for writing, props, wardrobe, locations, sound, legal, and safety teams.

The final report contains:

- a factual evidence ledger with `supported`, `contradicted`, `uncertain`, and `context needed` verdicts;
- source links for human review;
- continuity issues tied to scenes;
- department-specific production actions;
- a research-readiness score that does not judge artistic quality.

![ScriptProof report](docs/assets/scriptproof-report.png)

## Why this is agentic

One user action starts a bounded multi-step workflow. The agents decide which claims deserve research, formulate queries, call Parallel tools, evaluate conflicting evidence, preserve citations, compare scene logic, and assemble a handoff report. The user does not need to prompt each step.

## Architecture

```text
Screenplay + production context
              |
              v
      Script Analyst (Gemini)
              |
       structured research plan
              |
              v
  Evidence Researcher (Gemini + Parallel Search)
              |
       cited research bundle
              |
              v
       Story Editor (Gemini)
              |
              v
   Structured ScriptProof report
```

The three agents are orchestrated with Google ADK. Parallel's official `parallel-google-adk` package supplies typed `web_search` and `web_fetch` tools plus tool-call tracing. Before a report is returned, ScriptProof verifies that research claims triggered a Parallel call and that every public citation exactly matches a URL observed in a Parallel tool response. The Flask app renders validated Pydantic models rather than raw model HTML.

A deterministic source-quality gate removes blocked low-authority publisher classes before the editor sees the evidence. If a definitive verdict loses all acceptable sources, it is downgraded to `uncertain`. The Story Editor receives only controlled structured state and sanitized production context, never the raw prior-agent conversation.

See [the architecture note](docs/ARCHITECTURE.md) for trust boundaries and failure handling.

## Run locally

Requirements:

- Python 3.12
- a Google Cloud project with Vertex AI enabled
- Google Application Default Credentials
- a Parallel API key from [Parallel Platform](https://platform.parallel.ai/)

```bash
git clone https://github.com/simonlin1212/scriptproof-agent.git
cd scriptproof-agent
cp .env.example .env
uv sync --extra dev
```

Configure `.env` without committing it:

```dotenv
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=TRUE
SCRIPT_PROOF_MODEL=gemini-3.5-flash
PARALLEL_API_KEY=your-parallel-key
```

Authenticate and start the app:

```bash
gcloud auth application-default login
uv run python main.py
```

Open `http://127.0.0.1:8080` and use the included sample scene. The direct entry point intentionally bypasses Flask CLI's upward `.env` search, so a nested checkout cannot inherit a parent project's secrets.

## Live deployment

The judging deployment is live at [scriptproof-web](https://scriptproof-web-388088752401.asia-southeast1.run.app/). Paid analysis is protected by a reviewer code supplied with the judging instructions.

The service runs on Cloud Run with a dedicated least-privilege identity, Secret Manager-backed credentials, a 600-second request timeout, and a one-instance cost bound. The production smoke test completed with real Gemini 3.5 Flash and Parallel calls.

The intended production settings are documented in [the deployment runbook](docs/DEPLOYMENT.md).

## Testing

```bash
uv sync --extra dev
uv run ruff check .
uv run pytest --cov=scriptproof --cov-report=term-missing -q
```

The suite covers configuration drift, isolated environment loading, screenplay bounds, structured model contracts, Parallel call and citation provenance gates, deterministic source-quality filtering, editor context isolation, output validation, safe template rendering, API behavior, and reviewer access control. External Google and Parallel calls are mocked in unit tests; a live integration smoke test is run only with real credentials. Current verification is 47 passing tests and 89.00% coverage.

## Security and cost controls

- `.env` and credentials are ignored by Git.
- User input is length-bounded and normalized.
- Model output is validated through Pydantic and auto-escaped by Jinja.
- Citations must be HTTPS and must match URLs captured from actual Parallel tool responses.
- Blocked low-authority source classes are removed deterministically before editing and checked again before delivery.
- User-supplied production context is sanitized, bounded, and isolated from the Story Editor's instructions.
- API errors do not expose prompts, credentials, or provider responses.
- Production can require a reviewer access code to prevent anonymous users from consuming paid Gemini and Parallel calls.
- Cloud Run should use one bounded instance for the judging deployment.

## Hackathon

ScriptProof is submitted to the **Parallel track** of [Agentic Cinema: The Blockbuster Hackathon](https://agentic-cinema.devpost.com/). It uses Google Cloud AI exclusively for model and agent behavior and calls Parallel Search at runtime, matching the track's published requirements.

- [Devpost entry](https://devpost.com/software/scriptproof)
- [Live project](https://scriptproof-web-388088752401.asia-southeast1.run.app/)
- [Public 2:17 demo](https://youtu.be/hyHVu464XAM)

## Disclaimer

ScriptProof is a research and editorial aid, not legal, safety, historical, or production authority. Human department leads must review sources and decisions before a shoot.

## Support

If ScriptProof helps your production workflow, you can support continued open-source work:

<p align="center">
  <a href="https://buymeacoffee.com/simonlin1212"><img src="./assets/bmc-qr.png" width="180" alt="Buy Me a Coffee"></a>
</p>

## License

MIT License. See [LICENSE](LICENSE). Release history is recorded in [CHANGELOG.md](CHANGELOG.md).

**Author:** Simon Lin · X [@linsizhen](https://x.com/linsizhen) · Email: [simonlin0423@gmail.com](mailto:simonlin0423@gmail.com)
