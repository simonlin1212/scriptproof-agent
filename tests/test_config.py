import pytest

from scriptproof.config import (
    parse_script_limit,
    validate_location,
    validate_model,
)


def test_location_must_be_global_for_gemini_35():
    assert validate_location(" global ") == "global"
    with pytest.raises(RuntimeError, match="global"):
        validate_location("us-central1")


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
