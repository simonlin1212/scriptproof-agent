"""Boundary validation for screenplay submissions."""

from __future__ import annotations

import re

MIN_SCRIPT_CHARS = 120


class ScriptInputError(ValueError):
    """Raised when a screenplay cannot be accepted safely."""


def normalize_script(raw: str, *, max_chars: int) -> str:
    """Normalize plain-text screenplay input and enforce useful bounds."""
    normalized = raw.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in normalized.splitlines())
    normalized = re.sub(r"\n{4,}", "\n\n\n", normalized).strip()
    if len(normalized) < MIN_SCRIPT_CHARS:
        raise ScriptInputError(
            f"Please provide at least {MIN_SCRIPT_CHARS} characters of screenplay text."
        )
    if len(normalized) > max_chars:
        raise ScriptInputError(
            f"The screenplay exceeds the {max_chars:,}-character maximum."
        )
    return normalized
