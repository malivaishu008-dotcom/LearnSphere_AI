from models import db
from models.base import SerializableMixin, utcnow


class Syllabus(SerializableMixin, db.Model):
    __tablename__ = "syllabus"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    subject_code = db.Column(db.String(32), nullable=False)
    subject_name = db.Column(db.String(160), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(40), nullable=False)
    unit_title = db.Column(db.String(200), nullable=False)
    topics = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, default="", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
