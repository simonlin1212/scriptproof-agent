"""Deterministic source-quality gates for research and public reports."""

from __future__ import annotations

from urllib.parse import urlsplit

from scriptproof.models import ResearchBundle, ScriptReport

LOW_AUTHORITY_SOURCE_SUFFIXES = (
    "encyclopedia.com",
    "grokipedia.com",
    "justanswer.com",
    "wikipedia.org",
)


def is_low_authority_source(url: str) -> bool:
    """Match only the named host or one of its subdomains."""
    hostname = (urlsplit(url).hostname or "").lower().rstrip(".")
    return any(
        hostname == suffix or hostname.endswith(f".{suffix}")
        for suffix in LOW_AUTHORITY_SOURCE_SUFFIXES
    )


def sanitize_research_bundle(bundle: ResearchBundle) -> ResearchBundle:
    """Remove weak citations before the editor derives public conclusions."""
    sanitized_findings = []
    unresolved_questions = list(bundle.unresolved_questions)
    for finding in bundle.findings:
        strong_sources = [
            source
            for source in finding.sources
            if not is_low_authority_source(source.url)
        ]
        if strong_sources or finding.verdict not in {"supported", "contradicted"}:
            sanitized_findings.append(
                finding.model_copy(update={"sources": strong_sources})
            )
            continue
        unresolved_questions.append(
            f"Find an authoritative source for: {finding.claim}"
        )
        sanitized_findings.append(
            finding.model_copy(
                update={
                    "verdict": "uncertain",
                    "explanation": (
                        "Parallel returned only low-authority sources for this "
                        "claim, so ScriptProof cannot issue a definitive verdict."
                    ),
                    "recommendation": (
                        "Verify the claim with an archive, museum, government "
                        "source, university, or established trade publication."
                    ),
                    "sources": [],
                }
            )
        )
    return bundle.model_copy(
        update={
            "findings": sanitized_findings,
            "unresolved_questions": unresolved_questions[:8],
        }
    )


def validate_report_source_quality(report: ScriptReport) -> None:
    """Fail closed if the editor reintroduces a blocked public citation."""
    blocked = {
        source.url
        for finding in report.findings
        for source in finding.sources
        if is_low_authority_source(source.url)
    }
    if blocked:
        raise RuntimeError(
            "The final report contains low-authority citation(s): "
            + ", ".join(sorted(blocked))
        )
