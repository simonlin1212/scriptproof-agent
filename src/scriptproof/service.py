"""Flask interface for screenplay submission and report delivery."""

from __future__ import annotations

import asyncio
import hmac
import logging
import traceback
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request

from scriptproof.config import ACCESS_CODE, MAX_SCRIPT_CHARS
from scriptproof.input import ScriptInputError, normalize_script
from scriptproof.pipeline import ReportRun, generate_report

ReportGenerator = Callable[[str, str], Awaitable[ReportRun]]
logger = logging.getLogger(__name__)


def log_sanitized_exception(label: str, exc: Exception) -> None:
    """Keep diagnostic locations without logging provider-controlled messages."""
    frames = traceback.extract_tb(exc.__traceback__)
    locations = " > ".join(
        f"{Path(frame.filename).name}:{frame.lineno}:{frame.name}"
        for frame in frames[-8:]
    )
    logger.error("%s (%s) at %s", label, type(exc).__name__, locations or "unknown")


def create_app(
    *,
    report_generator: ReportGenerator = generate_report,
    max_chars: int = MAX_SCRIPT_CHARS,
    access_code: str = ACCESS_CODE,
) -> Flask:
    """Build the web application with an injectable analysis boundary."""
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = (max_chars * 12) + 4096

    def is_authorized(candidate: str) -> bool:
        return not access_code or hmac.compare_digest(candidate, access_code)

    @app.get("/health")
    def health():
        return jsonify({"service": "scriptproof", "status": "ok"})

    @app.get("/")
    def home():
        return render_template(
            "index.html", max_chars=max_chars, access_required=bool(access_code)
        )

    @app.post("/analyze")
    def analyze_form():
        raw_script = request.form.get("script_text", "")
        project_context = request.form.get("project_context", "").strip()[:1000]
        if not is_authorized(request.form.get("access_code", "")):
            return (
                render_template(
                    "index.html",
                    error="The reviewer access code is missing or incorrect.",
                    script_text=raw_script,
                    project_context=project_context,
                    max_chars=max_chars,
                    access_required=True,
                ),
                403,
            )
        try:
            script_text = normalize_script(raw_script, max_chars=max_chars)
            run = asyncio.run(report_generator(script_text, project_context))
        except ScriptInputError as exc:
            return (
                render_template(
                    "index.html",
                    error=str(exc),
                    script_text=raw_script,
                    project_context=project_context,
                    max_chars=max_chars,
                    access_required=bool(access_code),
                ),
                400,
            )
        except Exception as exc:
            log_sanitized_exception("ScriptProof analysis failed", exc)
            return (
                render_template(
                    "index.html",
                    error="The research run could not be completed. Please try again.",
                    script_text=raw_script,
                    project_context=project_context,
                    max_chars=max_chars,
                    access_required=bool(access_code),
                ),
                500,
            )
        return render_template("index.html", run=run, max_chars=max_chars)

    @app.post("/api/analyze")
    def analyze_api():
        if not is_authorized(request.headers.get("X-ScriptProof-Key", "")):
            return jsonify({"error": "Reviewer access denied."}), 403
        payload: Any = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "The JSON body must be an object."}), 400
        raw_script = payload.get("script_text", "")
        raw_context = payload.get("project_context", "")
        if not isinstance(raw_script, str) or not isinstance(raw_context, str):
            return (
                jsonify(
                    {"error": "script_text and project_context must be strings."}
                ),
                400,
            )
        try:
            script_text = normalize_script(raw_script, max_chars=max_chars)
            project_context = raw_context.strip()[:1000]
            run = asyncio.run(report_generator(script_text, project_context))
        except ScriptInputError as exc:
            return jsonify({"error": str(exc)}), 400
        except Exception as exc:
            log_sanitized_exception("ScriptProof API analysis failed", exc)
            return jsonify({"error": "The research run could not be completed."}), 500
        return jsonify(run.to_dict())

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "The request is larger than the allowed limit."}), 413

    return app
