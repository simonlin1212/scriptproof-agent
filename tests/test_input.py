import pytest

from scriptproof.input import ScriptInputError, normalize_script


def test_normalize_script_removes_nulls_and_normalizes_newlines():
    dialogue = "Hello from the archive. " * 6
    raw = f"INT. ROOM - DAY\r\n\r\nALEX\x00\r\n{dialogue}  "
    assert normalize_script(raw, max_chars=1000) == (
        f"INT. ROOM - DAY\n\nALEX\n{dialogue.rstrip()}"
    )


@pytest.mark.parametrize("raw", ["", "   ", "Too short."])
def test_normalize_script_rejects_missing_or_tiny_input(raw):
    with pytest.raises(ScriptInputError, match="at least"):
        normalize_script(raw, max_chars=1000)


def test_normalize_script_rejects_oversized_input():
    with pytest.raises(ScriptInputError, match="maximum"):
        normalize_script("A" * 1001, max_chars=1000)
