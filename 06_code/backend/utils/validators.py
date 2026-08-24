from datetime import datetime

from flask import request


def clean_json():
    if not request.is_json:
        raise ValueError("Request body must be JSON")
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("Request body must contain valid JSON")
    return data


def required(data, *fields):
    missing = [field for field in fields if not isinstance(data.get(field), str) or not data[field].strip()]
    if missing:
        raise ValueError("Required: " + ", ".join(missing))


def integer(value, label, minimum=None, maximum=None):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a whole number") from None
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError(f"{label} must be between {minimum} and {maximum}")
    return value


def valid_time(value, label):
    if not isinstance(value, str):
        raise ValueError(f"{label} must use HH:MM (24-hour) format")
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError(f"{label} must use HH:MM (24-hour) format") from None
    return value
