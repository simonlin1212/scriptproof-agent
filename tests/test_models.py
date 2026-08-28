import pytest
from pydantic import ValidationError

from scriptproof.models import (
    ContinuityIssue,
    EvidenceSource,
    ReportSummary,
    ResearchFinding,
    ScriptReport,
)


def make_report() -> ScriptReport:
    return ScriptReport(
        title="The Last Broadcast",
        logline="A radio host discovers tomorrow's emergency bulletin.",
        summary=ReportSummary(
            readiness_score=72,
            headline="Promising premise with two research risks.",
            strongest_element="The time-loop mechanics are easy to follow.",
            highest_priority="Verify period radio technology.",
        ),
        findings=[
            ResearchFinding(
                claim="Portable tape recorders were common in 1938.",
                verdict="contradicted",
                explanation="The depicted device predates commercial models.",
                recommendation="Replace it with an acetate disc recorder.",
                sources=[
                    EvidenceSource(
                        title="Museum collection",
                        url="https://example.org/recorder",
                    )
                ],
            )
        ],
        continuity_issues=[
            ContinuityIssue(
                severity="high",
                scenes=["2", "7"],
                issue="The locked door is opened without explanation.",
                recommendation="Add the key handoff in scene 5.",
            )
        ],
        production_notes=[],
        research_trace=[],
    )


def test_report_accepts_structured_cited_findings():
    report = make_report()
    assert report.summary.readiness_score == 72
    assert report.findings[0].sources[0].url.startswith("https://")


def test_source_rejects_non_https_url():
    with pytest.raises(ValidationError, match="HTTPS"):
        EvidenceSource(title="Unsafe", url="javascript:alert(1)")


def test_readiness_score_is_bounded():
    data = make_report().model_dump()
    data["summary"]["readiness_score"] = 101
    with pytest.raises(ValidationError):
        ScriptReport.model_validate(data)


@pytest.mark.parametrize("verdict", ["supported", "contradicted"])
def test_definitive_verdict_requires_a_source(verdict):
    with pytest.raises(ValidationError, match="source"):
        ResearchFinding(
            claim="The prop existed in 1938.",
            verdict=verdict,
            explanation="The evidence supports a definite verdict.",
            recommendation="Revise the prop description.",
            sources=[],
        )
