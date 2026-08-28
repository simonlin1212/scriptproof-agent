from datetime import UTC, datetime

import pytest

from scriptproof.models import ReportSummary, ScriptReport
from scriptproof.pipeline import ReportRun
from scriptproof.service import create_app


@pytest.fixture
def report_run() -> ReportRun:
    return ReportRun(
        run_id="demo-run",
        generated_at=datetime(2026, 8, 28, tzinfo=UTC),
        parallel_calls=3,
        report=ScriptReport(
            title="<script>alert(1)</script>",
            logline="A safe rendering test.",
            summary=ReportSummary(
                readiness_score=88,
                headline="Strong draft.",
                strongest_element="Clear stakes.",
                highest_priority="Verify the final date.",
            ),
            findings=[],
            continuity_issues=[],
            production_notes=[],
            research_trace=[],
        ),
    )


@pytest.fixture
def app(report_run):
    async def fake_generator(script_text: str, project_context: str = ""):
        assert "INT. ARCHIVE" in script_text
        return report_run

    return create_app(report_generator=fake_generator, max_chars=4000)


def test_health_is_available_without_credentials(app):
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "scriptproof", "status": "ok"}


def test_home_contains_product_promise(app):
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Research before the first take" in response.data


def test_analyze_renders_report_and_escapes_model_text(app):
    script = "INT. ARCHIVE - NIGHT\n" + ("A reel turns in the dark. " * 20)
    response = app.test_client().post(
        "/analyze",
        data={"script_text": script, "project_context": "1938 radio drama"},
    )
    assert response.status_code == 200
    assert b"demo-run" in response.data
    assert b"&lt;script&gt;alert(1)&lt;/script&gt;" in response.data
    assert b"<script>alert(1)</script>" not in response.data


def test_analyze_rejects_short_input(app):
    response = app.test_client().post("/analyze", data={"script_text": "short"})
    assert response.status_code == 400
    assert b"at least" in response.data


def test_api_analyze_returns_structured_json(app):
    script = "INT. ARCHIVE - NIGHT\n" + ("A reel turns in the dark. " * 20)
    response = app.test_client().post(
        "/api/analyze", json={"script_text": script, "project_context": "1938"}
    )
    assert response.status_code == 200
    assert response.get_json()["report"]["summary"]["readiness_score"] == 88


@pytest.mark.parametrize("payload", [[], "screenplay", 42])
def test_api_rejects_non_object_json(app, payload):
    response = app.test_client().post("/api/analyze", json=payload)
    assert response.status_code == 400
    assert response.get_json() == {"error": "The JSON body must be an object."}


@pytest.mark.parametrize(
    "payload",
    [
        {"script_text": 42},
        {"script_text": "A" * 200, "project_context": ["not", "text"]},
    ],
)
def test_api_rejects_non_string_fields(app, payload):
    response = app.test_client().post("/api/analyze", json=payload)
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "script_text and project_context must be strings."
    }


def test_access_code_protects_paid_analysis(report_run):
    async def fake_generator(script_text: str, project_context: str = ""):
        return report_run

    protected = create_app(
        report_generator=fake_generator,
        max_chars=4000,
        access_code="judge-only",
    )
    client = protected.test_client()
    script = "INT. ARCHIVE - NIGHT\n" + ("A reel turns in the dark. " * 20)

    denied = client.post("/analyze", data={"script_text": script})
    assert denied.status_code == 403

    allowed = client.post(
        "/analyze", data={"script_text": script, "access_code": "judge-only"}
    )
    assert allowed.status_code == 200

    api_denied = client.post("/api/analyze", json={"script_text": script})
    assert api_denied.status_code == 403
    api_allowed = client.post(
        "/api/analyze",
        json={"script_text": script},
        headers={"X-ScriptProof-Key": "judge-only"},
    )
    assert api_allowed.status_code == 200
