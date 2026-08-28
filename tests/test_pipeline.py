from datetime import UTC, datetime

import pytest

from scriptproof.models import ScriptReport
from scriptproof.pipeline import ReportRun, extract_report_from_state


def test_extract_report_from_state_validates_structured_output():
    state = {
        "final_report": {
            "title": "Signal Fire",
            "logline": "A projectionist receives a warning inside a lost reel.",
            "summary": {
                "readiness_score": 80,
                "headline": "A clear concept with manageable research gaps.",
                "strongest_element": "The visual motif is consistent.",
                "highest_priority": "Confirm nitrate film handling.",
            },
            "findings": [],
            "continuity_issues": [],
            "production_notes": [],
            "research_trace": [],
        }
    }
    report = extract_report_from_state(state)
    assert isinstance(report, ScriptReport)
    assert report.title == "Signal Fire"


def test_extract_report_from_state_requires_output():
    with pytest.raises(RuntimeError, match="final_report"):
        extract_report_from_state({})


def test_report_run_serializes_timestamp():
    report = extract_report_from_state(
        {
            "final_report": {
                "title": "Signal Fire",
                "logline": "A projectionist receives a warning inside a lost reel.",
                "summary": {
                    "readiness_score": 80,
                    "headline": "Ready for another pass.",
                    "strongest_element": "Visual logic.",
                    "highest_priority": "Film safety.",
                },
                "findings": [],
                "continuity_issues": [],
                "production_notes": [],
                "research_trace": [],
            }
        }
    )
    run = ReportRun(
        run_id="run-1",
        generated_at=datetime(2026, 8, 28, tzinfo=UTC),
        report=report,
        parallel_calls=2,
    )
    assert run.to_dict()["generated_at"] == "2026-08-28T00:00:00Z"
