"""Gunicorn and isolated local-development entry point."""

import os

from scriptproof.service import create_app

app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8080")),
        load_dotenv=False,
    )
