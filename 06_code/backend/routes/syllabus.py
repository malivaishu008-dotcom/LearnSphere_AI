from flask import Blueprint, request
from routes.common import error, parse_id, public_user_id, response
from flask_jwt_extended import jwt_required
from services.syllabus_service import service
from utils.validators import clean_json, integer, required

syllabus_bp = Blueprint("syllabus", __name__, url_prefix="/api/syllabus")


def values(data, partial=False):
    if not partial: required(data, "subject_code", "subject_name", "unit", "unit_title", "topics")
    result = {key: data[key].strip() for key in ("subject_code", "subject_name", "unit", "unit_title", "topics", "description") if key in data and isinstance(data[key], str)}
    if "semester" in data: result["semester"] = integer(data["semester"], "semester", 1, 12)
    elif not partial: result["semester"] = 1
    return result


@syllabus_bp.route("", methods=["GET", "POST"])
@jwt_required()
def collection():
    uid = public_user_id()
    if request.method == "GET":
        filters = {"semester": request.args.get("semester", type=int), "subject_name": request.args.get("subject"), "search": request.args.get("search")}
        return response([x.to_dict() for x in service.list(uid, filters, ("subject_code", "subject_name", "unit_title", "topics", "description"))], "Syllabus fetched successfully")
    try: record = service.create(uid, values(clean_json()))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "Syllabus created successfully", 201)


@syllabus_bp.route("/<record_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item(record_id):
    record = service.get(parse_id(record_id), public_user_id()) if parse_id(record_id) else None
    if not record: return error("Syllabus not found", 404, "NOT_FOUND")
    if request.method == "GET": return response(record.to_dict(), "Syllabus fetched successfully")
    if request.method == "DELETE": service.delete(record); return response(None, "Syllabus deleted successfully")
    try: record = service.update(record, values(clean_json(), True))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "Syllabus updated successfully")
