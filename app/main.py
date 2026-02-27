"""Flask application factory and routes."""

from __future__ import annotations

from flask import Flask, jsonify, render_template

from app.db import get_stories, init_db


def create_app() -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure DB tables exist before first request.
    init_db()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/stories")
    def api_stories():
        return jsonify(get_stories())

    return app

