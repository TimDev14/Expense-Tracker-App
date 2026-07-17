"""Unauthenticated endpoints useful for verifying the API is available."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    # TODO(Milestone 1): add an integration test confirming the frontend can
    # reach this public endpoint through the configured CORS origin.
    return jsonify(status="ok"), 200
