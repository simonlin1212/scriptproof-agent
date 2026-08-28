"""Gunicorn entry point."""

from scriptproof.service import create_app

app = create_app()
