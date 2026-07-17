"""Consistent JSON responses for API validation and missing records."""

from flask import jsonify


def error(message, status=400, fields=None):
    """Return a predictable error shape that the React client can display."""
    payload = {"error": message}
    if fields:
        payload["fields"] = fields
    return jsonify(payload), status
