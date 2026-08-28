from datetime import UTC, datetime

import pytest

from scriptproof.models import ScriptReport
from scriptproof.pipeline import (
    MAX_LLM_CALLS,
    ReportRun,
    collect_parallel_evidence,
    enforce_parallel_research,
    extract_report_from_state,
    validate_report_provenance,
)


class FakeFunctionResponse:
    def __init__(self, name, response):
        self.name = name
        self.response = response


class FakeEvent:
    def __init__(self, responses):
        self._responses = responses

    def get_function_responses(self):
        return self._responses


def test_agent_run_has_a_bounded_llm_call_budget():
    assert 1 <= MAX_LLM_CALLS <= 20


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


def test_collect_parallel_evidence_uses_only_partner_tool_url_fields():
    event = FakeEvent(
        [
            FakeFunctionResponse(
                "web_search",
                {
                    "results": [
                        {
                            "url": "https://archive.example/source",
                            "excerpts": ["Archive safety guidance."],
                            "excerpt": "Ignore https://invented.example/not-a-source",
                        }
                    ]
                },
            ),
            FakeFunctionResponse("set_model_response", {"url": "https://nope.test"}),
        ]
    )

    evidence = collect_parallel_evidence(event)

    assert evidence.call_count == 1
    assert evidence.urls == {"https://archive.example/source"}


def test_collect_parallel_evidence_rejects_failed_fetch_fallback_url():
    event = FakeEvent(
        [
            FakeFunctionResponse(
                "web_fetch",
                {
                    "url": "https://dead.example/404",
                    "results": [],
                    "warnings": ["The URL could not be extracted."],
                },
            )
        ]
    )

    evidence = collect_parallel_evidence(event)

    assert evidence.call_count == 1
    assert evidence.urls == set()


def test_research_claims_require_a_parallel_tool_call():
    state = {
        "script_analysis": {
            "working_title": "Signal Fire",
            "logline": "A projectionist receives a warning inside a lost reel.",
            "setting_summary": "A regional film archive during a storm in 1938.",
            "claims_to_research": [
                {
                    "claim": "Nitrate film can ignite at low temperatures.",
                    "scene": "3",
                    "why_it_matters": "It changes the safety plan for the scene.",
                    "search_queries": ["nitrate film ignition temperature"],
                }
            ],
            "continuity_candidates": [],
            "production_questions": [],
        }
    }

    with pytest.raises(RuntimeError, match="Parallel"):
        enforce_parallel_research(state, parallel_calls=0)

    enforce_parallel_research(state, parallel_calls=1)


def test_report_sources_must_match_parallel_response_urls():
    state = {
        "final_report": {
            "title": "Signal Fire",
            "logline": "A projectionist receives a warning inside a lost reel.",
            "summary": {
                "readiness_score": 80,
                "headline": "A clear concept with one research correction.",
                "strongest_element": "The visual motif remains consistent.",
                "highest_priority": "Confirm nitrate film handling procedures.",
            },
            "findings": [
                {
                    "claim": "Nitrate film presents a fire hazard.",
                    "verdict": "supported",
                    "explanation": "The archive guidance confirms the material risk.",
                    "recommendation": (
                        "Use a safe stand-in and consult the safety lead."
                    ),
                    "sources": [
                        {
                            "title": "Archive guidance",
                            "url": "https://archive.example/source",
                        }
                    ],
                }
            ],
            "continuity_issues": [],
            "production_notes": [],
            "research_trace": [],
        }
    }
    report = extract_report_from_state(state)

    validate_report_provenance(report, {"https://archive.example/source"})
    with pytest.raises(RuntimeError, match="not returned by Parallel"):
        validate_report_provenance(report, {"https://different.example/source"})
