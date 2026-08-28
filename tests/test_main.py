import runpy
from pathlib import Path

from flask import Flask


def test_local_entry_point_disables_flask_parent_dotenv_search(monkeypatch):
    run_arguments = {}

    def fake_run(self, **kwargs):
        run_arguments.update(kwargs)

    monkeypatch.setattr(Flask, "run", fake_run)
    runpy.run_path(
        Path(__file__).resolve().parents[1] / "main.py",
        run_name="__main__",
    )

    assert run_arguments["load_dotenv"] is False
