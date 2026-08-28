# ScriptProof submission copy

## Links

- Live project: https://scriptproof-web-388088752401.asia-southeast1.run.app/
- Public source: https://github.com/simonlin1212/scriptproof-agent
- Demo video: https://youtu.be/hyHVu464XAM

## Tagline

A pre-production agent that checks screenplay facts, catches continuity breaks, and returns a cited revision brief.

## Inspiration

Most screenplay tools help writers generate more pages. ScriptProof starts with a different problem: a small factual mistake can become an expensive prop, location, sound, legal, or safety problem once a crew begins production. Writers and small teams need a research pass they can audit, not another chat window that gives confident answers without showing its work.

## What it does

ScriptProof reads plain screenplay text and optional production context. One action starts a three-agent workflow:

1. The Script Analyst selects at most five claims that can change a production decision and identifies cross-scene continuity questions.
2. The Evidence Researcher calls Parallel Search and Fetch at runtime, evaluates the returned material, and keeps the source URLs.
3. The Story Editor turns that evidence and the scene logic into a research-readiness score, claim-level verdicts, continuity issues, and department actions.

The final report is meant to be used. A props lead sees what object must change. A writer sees the scenes that conflict. A sound designer gets the period detail to reproduce. Supported and contradicted findings link back to the sources used.

## How it was built

Google ADK runs the sequential agent workflow. All three agents use Gemini 3.5 Flash through Vertex AI in the `global` model location. The Evidence Researcher uses Parallel's official `parallel-google-adk` Search and Fetch tools. Flask renders validated Pydantic models on Cloud Run.

The production path has several fail-closed checks:

- A screenplay with research claims cannot return a report unless a Parallel tool call completed.
- Every public citation must exactly match a URL observed in a successful Parallel response.
- A deterministic quality gate removes blocked low-authority publisher classes before the editor sees the evidence.
- If filtering removes the only evidence for a definitive verdict, ScriptProof changes that verdict to `uncertain`.
- The Story Editor receives controlled structured state and sanitized production context instead of the raw prior-agent conversation.

The hosted service uses a dedicated runtime identity, Secret Manager, a reviewer code for the paid endpoint, a 600-second request timeout, and a one-instance cost limit.

## Data sources

ScriptProof does not ship with a fixed research database. The Evidence Researcher creates queries from each screenplay and calls Parallel at runtime. The accepted demo run used six Parallel calls and preserved six sources, including the Computer History Museum, Library of Congress, United States Senate, and The New York Times.

## Interesting findings from the demo

The sample screenplay takes place in a US radio studio in 1938. ScriptProof found that its portable magnetic tape recorder was anachronistic and recommended a period transcription disc recorder. It also found that the dial-tone detail was plausible, while flagging the contradiction between a working tone and dialogue saying the lines were down.

The continuity pass caught two more production questions: a locked door opens after the only key disappears with a character, and a scene marked "later" shows the clock moving backward. The report assigns the resulting work to props, writing, and sound.

## Challenges

Citation-looking text was not enough. The app needed to prove that every displayed URL came from a real partner tool response. ADK conversation history also required careful handling: the final editor should see the validated research records, but not inherit raw researcher text or treat production notes as instructions. A third challenge was source quality. Prompt wording improved the results, but only deterministic filtering made the rule enforceable.

## Accomplishments

- A working hosted product rather than a mock or chat prototype.
- Real Gemini 3.5 Flash and Parallel calls in the production path.
- Exact citation provenance, source-quality filtering, and editor-context isolation.
- A responsive report designed for actual pre-production handoff.
- 47 automated tests, 89% coverage, desktop and mobile browser QA, and independent pre-push review.

## What I learned

Agent reliability depends on the boundaries around the model. Structured output helps, but runtime evidence matters more: tool calls must be traced, URLs must be compared, and weak evidence must remain uncertain. I also learned that a useful creative agent should end with decisions a crew can act on. A long answer is not the same thing as a production brief.

## What's next

The next product version can accept screenplay PDF and Final Draft files, preserve scene identifiers across revisions, and export department-specific checklists. Firestore can add private report history without changing the three agent contracts. The current hackathon version stays focused on one auditable job: research the draft before the first take.

## Built with

- Google Cloud Run
- Vertex AI
- Gemini 3.5 Flash
- Google ADK
- Parallel Search and Fetch
- Python 3.12
- Flask
- Pydantic
