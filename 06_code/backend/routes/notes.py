from flask import Blueprint, request
from routes.common import error, parse_id, public_user_id, response
from flask_jwt_extended import jwt_required
from routes.uploads import optional_pdf
from services.note_service import service
from utils.validators import clean_json, integer, required

notes_bp = Blueprint("notes", __name__, url_prefix="/api/notes")


@notes_bp.post("/upload")
@jwt_required()
def upload():
    try:
        file_url = optional_pdf("notes")
    except ValueError as exc:
        return error(str(exc))
    if not file_url:
        return error("Choose a PDF file to upload")
    return response({"file_url": file_url}, "Note PDF uploaded successfully", 201)


def note_values(data, partial=False):
    if not partial:
        required(data, "title")
    values = {key: data[key].strip() for key in ("title", "subject", "topic", "description", "content") if key in data and isinstance(data[key], str)}
    if "body" in data and isinstance(data["body"], str):
        values["body"] = data["body"].strip()
        values.setdefault("content", values["body"])
    if not partial:
        values.setdefault("subject", "General")
        values.setdefault("topic", "General")
    if "semester" in data:
        values["semester"] = integer(data["semester"], "semester", 1, 12)
    elif not partial:
        values["semester"] = 1
    return values


@notes_bp.route("", methods=["GET", "POST"])
@jwt_required()
def collection():
    uid = public_user_id()
    if request.method == "GET":
        filters = {"subject": request.args.get("subject"), "semester": request.args.get("semester", type=int), "topic": request.args.get("topic"), "search": request.args.get("search")}
        return response([item.to_dict() for item in service.list(uid, filters, ("title", "subject", "topic", "description", "content"))], "Notes fetched successfully")
    try:
        data = clean_json()
        record = service.create(uid, note_values(data))
    except ValueError as exc:
        return error(str(exc))
    return response(record.to_dict(), "Note created successfully", 201)


@notes_bp.route("/<note_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item(note_id):
    record = service.get(parse_id(note_id), public_user_id()) if parse_id(note_id) else None
    if not record:
        return error("Note not found", 404, "NOT_FOUND")
    if request.method == "GET":
        return response(record.to_dict(), "Note fetched successfully")
    if request.method == "DELETE":
        service.delete(record)
        return response(None, "Note deleted successfully")
    try:
        record = service.update(record, note_values(clean_json(), partial=True))
    except ValueError as exc:
        return error(str(exc))
    return response(record.to_dict(), "Note updated successfully")
