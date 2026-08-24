from datetime import datetime

from flask import Blueprint, request
from routes.common import error, parse_id, public_user_id, response
from flask_jwt_extended import jwt_required
from routes.uploads import optional_pdf
from services.pyq_service import service
from utils.validators import clean_json, integer, required

pyq_bp = Blueprint("pyq", __name__, url_prefix="/api/pyq")


@pyq_bp.post("/upload")
@jwt_required()
def upload():
    try:
        file_url = optional_pdf("pyq")
    except ValueError as exc:
        return error(str(exc))
    if not file_url:
        return error("Choose a PDF file to upload")
    return response({"file_url": file_url}, "PYQ PDF uploaded successfully", 201)


def values(data, partial=False):
    if not partial: required(data, "subject", "subject_code", "exam_type")
    result = {key: data[key].strip() for key in ("subject", "subject_code", "exam_type", "question", "unit", "file_url") if key in data and isinstance(data[key], str)}
    if "semester" in data: result["semester"] = integer(data["semester"], "semester", 1, 12)
    elif not partial: result["semester"] = 1
    if "exam_year" in data: result["exam_year"] = integer(data["exam_year"], "exam_year", 1900, datetime.now().year + 1)
    elif not partial: raise ValueError("Required: exam_year")
    if "marks" in data and data["marks"] not in (None, ""): result["marks"] = integer(data["marks"], "marks", 0, 1000)
    return result


@pyq_bp.route("", methods=["GET", "POST"])
@jwt_required()
def collection():
    uid = public_user_id()
    if request.method == "GET":
        filters = {"subject": request.args.get("subject"), "semester": request.args.get("semester", type=int), "exam_year": request.args.get("year", type=int), "exam_type": request.args.get("exam_type"), "search": request.args.get("search")}
        return response([x.to_dict() for x in service.list(uid, filters, ("subject", "subject_code", "question", "exam_type", "unit"))], "PYQs fetched successfully")
    try: record = service.create(uid, values(clean_json()))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "PYQ created successfully", 201)


@pyq_bp.route("/<record_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item(record_id):
    record = service.get(parse_id(record_id), public_user_id()) if parse_id(record_id) else None
    if not record: return error("PYQ not found", 404, "NOT_FOUND")
    if request.method == "GET": return response(record.to_dict(), "PYQ fetched successfully")
    if request.method == "DELETE": service.delete(record); return response(None, "PYQ deleted successfully")
    try: record = service.update(record, values(clean_json(), True))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "PYQ updated successfully")
