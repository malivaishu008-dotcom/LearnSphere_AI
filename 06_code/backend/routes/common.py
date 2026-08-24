
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def response(data=None, message="Success", status=200):
    return jsonify({"success": True, "message": message, "data": data}), status


def error(message, status=400, code="VALIDATION_ERROR"):
    return jsonify({"success": False, "message": message, "error": code}), status


def public_user_id():
    """Return the authenticated user's id when present, otherwise 0.

    This keeps demo-friendly public access when unauthenticated, but ensures
    authenticated requests map to the correct user so their private data is
    returned. Uses optional JWT verification from flask_jwt_extended.
    """
    try:
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        return int(identity) if identity else 0
    except Exception:
        return 0


def parse_id(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None
