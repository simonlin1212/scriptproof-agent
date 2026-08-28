"""Execute one ScriptProof analysis pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from parallel_google_adk import ParallelTracingPlugin

from scriptproof.agent import root_agent
from scriptproof.models import ScriptReport

APP_NAME = "scriptproof"
USER_ID = "web-reviewer"


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
    async for _event in active_runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        pass

    final_session = await active_session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session.id,
    )
    if final_session is None:
        raise RuntimeError("Agent pipeline completed without a session.")
    report = extract_report_from_state(final_session.state)
    parallel_trace = final_session.state.get("_parallel_calls", [])
    return ReportRun(
        run_id=f"sp-{uuid4().hex[:12]}",
        generated_at=datetime.now(UTC),
        report=report,
        parallel_calls=len(parallel_trace) if isinstance(parallel_trace, list) else 0,
    )
