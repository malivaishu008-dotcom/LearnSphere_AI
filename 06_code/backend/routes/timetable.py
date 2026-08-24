from datetime import datetime

from flask import Blueprint, request
from routes.common import error, parse_id, public_user_id, response
from flask_jwt_extended import jwt_required
from services.timetable_service import service
from utils.validators import clean_json, integer, required, valid_time

timetable_bp = Blueprint("timetable", __name__, url_prefix="/api/timetable")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def values(data, partial=False):
    if not partial: required(data, "day", "subject", "subject_code", "start_time", "end_time")
    result = {key: data[key].strip() for key in ("day", "subject", "subject_code", "room", "faculty") if key in data and isinstance(data[key], str)}
    if "day" in result and result["day"] not in DAYS: raise ValueError("day must be a valid weekday")
    if "semester" in data: result["semester"] = integer(data["semester"], "semester", 1, 12)
    elif not partial: result["semester"] = 1
    for field in ("start_time", "end_time"):
        if field in data: result[field] = valid_time(data[field], field)
    if "start_time" in result and "end_time" in result and result["start_time"] >= result["end_time"]:
        raise ValueError("end_time must be later than start_time")
    return result


@timetable_bp.get("/today")
@jwt_required()
def today():
    day = datetime.now().strftime("%A")
    records = service.list(public_user_id(), {"day": day})
    return response([x.to_dict() for x in records], f"Today's timetable ({day}) fetched successfully")


@timetable_bp.route("", methods=["GET", "POST"])
@jwt_required()
def collection():
    uid = public_user_id()
    if request.method == "GET":
        filters = {"semester": request.args.get("semester", type=int), "day": request.args.get("day"), "subject": request.args.get("subject"), "search": request.args.get("search")}
        return response([x.to_dict() for x in service.list(uid, filters, ("subject", "subject_code", "room", "faculty"))], "Timetable fetched successfully")
    try: record = service.create(uid, values(clean_json()))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "Timetable entry created successfully", 201)


@timetable_bp.route("/<record_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def item(record_id):
    record = service.get(parse_id(record_id), public_user_id()) if parse_id(record_id) else None
    if not record: return error("Timetable entry not found", 404, "NOT_FOUND")
    if request.method == "GET": return response(record.to_dict(), "Timetable entry fetched successfully")
    if request.method == "DELETE": service.delete(record); return response(None, "Timetable entry deleted successfully")
    try: record = service.update(record, values(clean_json(), True))
    except ValueError as exc: return error(str(exc))
    return response(record.to_dict(), "Timetable entry updated successfully")
