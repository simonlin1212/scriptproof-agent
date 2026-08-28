import pytest

import scriptproof.config as config
from scriptproof.config import (
    load_project_dotenv,
    parse_script_limit,
    validate_location,
    validate_model,
)


def test_location_must_be_global_for_gemini_35():
    assert validate_location("global") == "global"
    for value in (" global ", "GLOBAL", "us-central1"):
        with pytest.raises(RuntimeError, match="global"):
            validate_location(value)


def test_dotenv_loader_never_searches_parent_directories(monkeypatch, tmp_path):
    loaded_paths = []

    def fake_load_dotenv(*, dotenv_path, override):
        loaded_paths.append((dotenv_path, override))
        return False

    monkeypatch.setattr(config, "load_dotenv", fake_load_dotenv)
    dotenv_path = load_project_dotenv(tmp_path)

    assert dotenv_path == tmp_path / ".env"
    assert loaded_paths == [(tmp_path / ".env", False)]


@pytest.mark.parametrize("model", ["gemini-3.5-flash", "gemini-3.5-pro"])
def test_model_accepts_google_gemini(model):
    assert validate_model(model) == model


@pytest.mark.parametrize("model", ["gpt-5", "claude-opus", "gemini-2.5-flash"])
def test_model_rejects_noncompliant_or_old_ai(model):
    with pytest.raises(RuntimeError, match="Gemini 3.5"):
        validate_model(model)


def test_script_limit_is_bounded():
    assert parse_script_limit("40000") == 40000
    for value in ("not-a-number", "999", "200001"):
        with pytest.raises(RuntimeError, match="SCRIPT_PROOF_MAX_CHARS"):
            parse_script_limit(value)
