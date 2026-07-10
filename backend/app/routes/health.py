"""Unauthenticated endpoints useful for verifying the API is available."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    return jsonify(status="ok"), 200
