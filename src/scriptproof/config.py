"""Runtime configuration and competition compliance gates."""

from __future__ import annotations

import os
import re

from dotenv import load_dotenv

load_dotenv()


def validate_location(value: str) -> str:
    """Require the Vertex location that serves the selected Gemini model."""
    location = value.strip().lower()
    if location != "global":
        raise RuntimeError(
            "GOOGLE_CLOUD_LOCATION must be 'global' for Gemini 3.5; "
            f"received {value!r}."
        )
    return location


def validate_model(value: str) -> str:
    """Keep the project on eligible Google AI and reject accidental drift."""
    model = value.strip()
    match = re.fullmatch(r"gemini-(\d+)\.(\d+)(?:-[a-z0-9.-]+)?", model)
    if match is None or tuple(map(int, match.groups())) < (3, 5):
        raise RuntimeError(
            "ScriptProof requires a Google Gemini 3.5 or newer model; "
            f"received {value!r}."
        )
    return model


def parse_script_limit(value: str) -> int:
    """Parse a bounded screenplay input limit."""
    try:
        limit = int(value)
    except ValueError as exc:
        raise RuntimeError(
            "SCRIPT_PROOF_MAX_CHARS must be an integer from 1000 to 200000."
        ) from exc
    if not 1000 <= limit <= 200_000:
        raise RuntimeError(
            "SCRIPT_PROOF_MAX_CHARS must be an integer from 1000 to 200000."
        )
    return limit


MODEL = validate_model(os.getenv("SCRIPT_PROOF_MODEL", "gemini-3.5-flash"))
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
GOOGLE_CLOUD_LOCATION = validate_location(
    os.getenv("GOOGLE_CLOUD_LOCATION", "global")
)
MAX_SCRIPT_CHARS = parse_script_limit(
    os.getenv("SCRIPT_PROOF_MAX_CHARS", "40000")
)
ACCESS_CODE = os.getenv("SCRIPT_PROOF_ACCESS_CODE", "").strip()
