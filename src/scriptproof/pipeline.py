"""Execute one ScriptProof analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from parallel_google_adk import ParallelTracingPlugin

from scriptproof.agent import root_agent
from scriptproof.models import ScriptAnalysis, ScriptReport

APP_NAME = "scriptproof"
USER_ID = "web-reviewer"
PARALLEL_TOOL_NAMES = frozenset({"web_search", "web_fetch"})


@dataclass(slots=True)
class ParallelEvidence:
    """Partner tool calls and source URLs observed in ADK events."""

    call_count: int = 0
    urls: set[str] = field(default_factory=set)


@dataclass(frozen=True, slots=True)
class ReportRun:
    """One completed analysis with operational metadata."""

    run_id: str
    generated_at: datetime
    report: ScriptReport
    parallel_calls: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "generated_at": self.generated_at.isoformat().replace("+00:00", "Z"),
            "parallel_calls": self.parallel_calls,
            "report": self.report.model_dump(mode="json"),
        }


def extract_report_from_state(state: dict[str, Any]) -> ScriptReport:
    """Validate the final agent output before exposing it to the interface."""
    raw_report = state.get("final_report")
    if not raw_report:
        raise RuntimeError("Agent pipeline completed without final_report output.")
    return ScriptReport.model_validate(raw_report)


def _successful_parallel_urls(tool_name: str, value: Any) -> set[str]:
    """Collect URLs only from successful partner result records."""
    if hasattr(value, "model_dump"):
        value = value.model_dump()
    if not isinstance(value, dict):
        return set()
    if tool_name == "web_search":
        results = value.get("results")
        if not isinstance(results, list):
            return set()
        urls = {
            item["url"].strip()
            for item in results
            if isinstance(item, dict) and isinstance(item.get("url"), str)
        }
    elif tool_name == "web_fetch":
        url = value.get("url")
        excerpts = value.get("excerpts")
        if not isinstance(url, str) or not isinstance(excerpts, list):
            return set()
        urls = {url.strip()}
    else:
        return set()
    return {url for url in urls if url.startswith("https://")}


def collect_parallel_evidence(
    event: Any, evidence: ParallelEvidence | None = None
) -> ParallelEvidence:
    """Capture successful Parallel tool responses from one ADK event."""
    collected = evidence or ParallelEvidence()
    get_responses = getattr(event, "get_function_responses", None)
    if not callable(get_responses):
        return collected
    for response in get_responses() or []:
        tool_name = getattr(response, "name", None)
        if tool_name not in PARALLEL_TOOL_NAMES:
            continue
        collected.call_count += 1
        collected.urls.update(
            _successful_parallel_urls(tool_name, getattr(response, "response", None))
        )
    return collected


def enforce_parallel_research(state: dict[str, Any], parallel_calls: int) -> None:
    """Reject a researched run that completed without the partner API."""
    raw_analysis = state.get("script_analysis")
    if not raw_analysis:
        raise RuntimeError("Agent pipeline completed without script_analysis output.")
    analysis = ScriptAnalysis.model_validate(raw_analysis)
    if analysis.claims_to_research and parallel_calls < 1:
        raise RuntimeError(
            "The screenplay had research claims, but no Parallel tool call completed."
        )


def validate_report_provenance(report: ScriptReport, parallel_urls: set[str]) -> None:
    """Require every public citation to come from an observed Parallel response."""
    cited_urls = {
        source.url for finding in report.findings for source in finding.sources
    }
    unverified = cited_urls - parallel_urls
    if unverified:
        raise RuntimeError(
            "The report cited URL(s) not returned by Parallel: "
            + ", ".join(sorted(unverified))
        )


async def generate_report(
    script_text: str,
    project_context: str = "",
    *,
    runner: Runner | None = None,
) -> ReportRun:
    """Run the analyst, Parallel researcher, and editor in sequence."""
    session_service = InMemorySessionService()
    active_runner = runner or Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        plugins=[ParallelTracingPlugin()],
    )
    active_session_service = active_runner.session_service
    session = await active_session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    context = project_context.strip() or "No additional production context supplied."
    request = (
        "Analyze this screenplay for factual research and continuity readiness.\n\n"
        f"PRODUCTION CONTEXT\n{context}\n\nSCREENPLAY\n{script_text}"
    )
    message = types.Content(role="user", parts=[types.Part(text=request)])
    parallel_evidence = ParallelEvidence()
    async for event in active_runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        collect_parallel_evidence(event, parallel_evidence)

    final_session = await active_session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session.id,
    )
    if final_session is None:
        raise RuntimeError("Agent pipeline completed without a session.")
    enforce_parallel_research(final_session.state, parallel_evidence.call_count)
    report = extract_report_from_state(final_session.state)
    validate_report_provenance(report, parallel_evidence.urls)
    return ReportRun(
        run_id=f"sp-{uuid4().hex[:12]}",
        generated_at=datetime.now(UTC),
        report=report,
        parallel_calls=parallel_evidence.call_count,
    )
