from models import db
from models.base import SerializableMixin, utcnow


class Timetable(SerializableMixin, db.Model):
    __tablename__ = "timetable"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    day = db.Column(db.String(12), nullable=False)
    subject = db.Column(db.String(160), nullable=False)
    subject_code = db.Column(db.String(32), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    room = db.Column(db.String(80), default="", nullable=False)
    faculty = db.Column(db.String(160), default="", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
