# Agentic Cinema compliance checklist

Sources checked on 2026-08-28:

- [Hackathon overview](https://agentic-cinema.devpost.com/)
- [Official rules](https://agentic-cinema.devpost.com/rules)
- [Hackathon resources](https://agentic-cinema.devpost.com/resources)
- [Parallel track resources](https://agentic-cinema.devpost.com/details/parallel-resources)

## Eligibility and timing

- Hong Kong is not named in the published exclusion list.
- Submission deadline: 2026-09-10 05:00 Asia/Singapore.
- The project must be newly created during the contest period.

## Product requirements

- Functional, production-ready AI agent or multi-agent network.
- Targets a real workflow for filmmakers, screenwriters, studio crews, or fans.
- Runs on web, Android, or iOS.
- Uses Gemini and Google Cloud Agent Builder / accepted Google packages at runtime.
- Uses the selected partner service at runtime.

## Parallel track requirement

The source code must actively use Parallel Search at runtime through an accepted SDK, MCP, or grounding integration. ScriptProof uses the official `parallel-google-adk` package and exposes its typed `web_search` and `web_fetch` tools to the evidence researcher.

## AI restriction

Only Google Cloud artificial intelligence tools and the selected partner's built-in AI capabilities may be used. ScriptProof must not add OpenAI, Anthropic, AWS AI, Microsoft AI, or an external agent framework.

## Submission package

- Hosted project URL for judging.
- English description covering features, technology, data sources, findings, and learnings.
- Public repository with all source, assets, setup instructions, and an open-source license.
- Visible runtime imports and calls for Google Cloud and Parallel.
- Public YouTube or Vimeo demo, no longer than three minutes, in English or with English subtitles.
- Parallel track selected in Devpost.

## Judging

The four criteria are equally weighted:

1. Technological implementation.
2. Complete and coherent product design.
3. Credible impact on a specific audience and problem.
4. Creative, non-obvious idea with real problem understanding.
