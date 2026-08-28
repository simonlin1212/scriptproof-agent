# Changelog

All notable changes to ScriptProof are documented here.

## [Unreleased] - 2026-08-28

### Added

- Three-stage Google ADK screenplay analysis workflow.
- Runtime Parallel Search integration with exact citation provenance checks.
- Server-rendered review interface, JSON API, sample screenplay, and Cloud Run packaging.
- Reviewer access code, bounded inputs, structured-output validation, and security checks.

### Fixed

- Prevented local configuration from inheriting a parent repository's `.env`.
- Bypassed Flask CLI's parent-directory dotenv search in the documented local entry point.
- Rejected researched runs that complete without a Parallel tool call.
- Rejected citations not present in observed Parallel responses.
- Excluded failed `web_fetch` fallback URLs from the verified citation set.
- Returned HTTP 400 for malformed JSON request shapes and field types.
- Required the canonical Vertex AI location value `global`.
