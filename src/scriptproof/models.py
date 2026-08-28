"""Structured contracts shared by the agents, API, and interface."""

from __future__ import annotations

from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, Field, field_validator, model_validator

Verdict = Literal["supported", "contradicted", "uncertain", "context_needed"]
Severity = Literal["high", "medium", "low"]


class ClaimToResearch(BaseModel):
    """One externally verifiable statement found in a screenplay."""

    claim: str = Field(min_length=5, max_length=500)
    scene: str = Field(min_length=1, max_length=80)
    why_it_matters: str = Field(min_length=5, max_length=500)
    search_queries: list[str] = Field(min_length=1, max_length=3)


class ContinuityIssue(BaseModel):
    """A possible contradiction across scenes."""

    severity: Severity
    scenes: list[str] = Field(min_length=1, max_length=6)
    issue: str = Field(min_length=5, max_length=800)
    recommendation: str = Field(min_length=5, max_length=800)


class ProductionNote(BaseModel):
    """A practical note for writing or pre-production."""

    department: Literal[
        "writing", "art", "wardrobe", "props", "locations", "sound", "legal", "safety"
    ]
    note: str = Field(min_length=5, max_length=800)
    action: str = Field(min_length=5, max_length=800)


class ScriptAnalysis(BaseModel):
    """Internal first-pass reading produced before web research."""

    working_title: str = Field(min_length=1, max_length=160)
    logline: str = Field(min_length=10, max_length=600)
    setting_summary: str = Field(min_length=10, max_length=800)
    claims_to_research: list[ClaimToResearch] = Field(max_length=5)
    continuity_candidates: list[ContinuityIssue] = Field(max_length=8)
    production_questions: list[str] = Field(max_length=8)


class EvidenceSource(BaseModel):
    """A human-reviewable source returned by Parallel research."""

    title: str = Field(min_length=1, max_length=300)
    url: str = Field(min_length=10, max_length=2048)

    @field_validator("url")
    @classmethod
    def require_https(cls, value: str) -> str:
        parsed = urlsplit(value.strip())
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("Evidence URLs must use HTTPS.")
        return value.strip()


class ResearchFinding(BaseModel):
    """A claim-level verdict supported by cited web evidence."""

    claim: str = Field(min_length=5, max_length=500)
    verdict: Verdict
    explanation: str = Field(min_length=10, max_length=1600)
    recommendation: str = Field(min_length=5, max_length=1000)
    sources: list[EvidenceSource] = Field(max_length=5)

    @model_validator(mode="after")
    def require_evidence_for_definitive_verdict(self) -> ResearchFinding:
        if self.verdict in {"supported", "contradicted"} and not self.sources:
            raise ValueError("A definitive verdict requires at least one source.")
        return self


class ResearchBundle(BaseModel):
    """Parallel-grounded research output passed to the editor agent."""

    findings: list[ResearchFinding] = Field(max_length=5)
    unresolved_questions: list[str] = Field(max_length=8)
    queries_run: list[str] = Field(max_length=15)


class ReportSummary(BaseModel):
    """At-a-glance editorial assessment."""

    readiness_score: int = Field(ge=0, le=100)
    headline: str = Field(min_length=5, max_length=300)
    strongest_element: str = Field(min_length=5, max_length=500)
    highest_priority: str = Field(min_length=5, max_length=500)


class ScriptReport(BaseModel):
    """Final structured deliverable shown to writers and production teams."""

    title: str = Field(min_length=1, max_length=160)
    logline: str = Field(min_length=10, max_length=600)
    summary: ReportSummary
    findings: list[ResearchFinding] = Field(max_length=5)
    continuity_issues: list[ContinuityIssue] = Field(max_length=8)
    production_notes: list[ProductionNote] = Field(max_length=8)
    research_trace: list[str] = Field(max_length=15)
