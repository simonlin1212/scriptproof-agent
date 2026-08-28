"""Google ADK multi-agent network for ScriptProof."""

from google.adk.agents import LlmAgent, SequentialAgent
from parallel_google_adk import web_fetch, web_search

from scriptproof.config import MODEL
from scriptproof.models import ResearchBundle, ScriptAnalysis, ScriptReport
from scriptproof.prompts import ANALYZE_SCRIPT, EDIT_REPORT, RESEARCH_CLAIMS

script_analyst = LlmAgent(
    name="script_analyst",
    model=MODEL,
    description="Reads a screenplay and creates a bounded research plan.",
    instruction=ANALYZE_SCRIPT,
    output_key="script_analysis",
    output_schema=ScriptAnalysis,
)

evidence_researcher = LlmAgent(
    name="evidence_researcher",
    model=MODEL,
    description="Uses Parallel search to verify screenplay claims with citations.",
    instruction=RESEARCH_CLAIMS,
    tools=[web_search, web_fetch],
    output_key="research_bundle",
    output_schema=ResearchBundle,
)

story_editor = LlmAgent(
    name="story_editor",
    model=MODEL,
    description="Turns analysis and evidence into a production-ready report.",
    instruction=EDIT_REPORT,
    output_key="final_report",
    output_schema=ScriptReport,
)

root_agent = SequentialAgent(
    name="scriptproof",
    description="Analyze a screenplay, research its claims, and edit the final report.",
    sub_agents=[script_analyst, evidence_researcher, story_editor],
)
