"""Small dependency-free request validators for the JSON API."""

from datetime import date
import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def required_string(data, field, minimum=1, maximum=255):
    value = data.get(field)
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        return None, f"{field} must be between {minimum} and {maximum} characters."
    return value.strip(), None


def optional_string(data, field, maximum=255):
    value = data.get(field, "")
    if value is None:
        return None, None
    if not isinstance(value, str) or len(value.strip()) > maximum:
        return None, f"{field} must be at most {maximum} characters."
    return value.strip(), None


def positive_integer(data, field):
    value = data.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None, f"{field} must be a positive integer in minor currency units."
    return value, None


def validate_month(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}", value):
        return None, "month must use YYYY-MM format."
    try:
        date.fromisoformat(f"{value}-01")
    except ValueError:
        return None, "month must be a real calendar month."
    return value, None


def validate_date(value):
    if not isinstance(value, str):
        return None, "date must use YYYY-MM-DD format."
    try:
        return date.fromisoformat(value), None
    except ValueError:
        return None, "date must be a real YYYY-MM-DD date."


def validation_errors(**checks):
    """Return a compact field-to-message map after collecting validations."""
    return {field: message for field, (_, message) in checks.items() if message}
