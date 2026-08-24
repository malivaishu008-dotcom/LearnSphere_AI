from models import db
from models.base import SerializableMixin, utcnow


class PYQ(SerializableMixin, db.Model):
    __tablename__ = "pyq"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    subject = db.Column(db.String(160), nullable=False)
    subject_code = db.Column(db.String(32), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    exam_year = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(80), nullable=False)
    question = db.Column(db.Text, default="", nullable=False)
    marks = db.Column(db.Integer, nullable=True)
    unit = db.Column(db.String(40), nullable=True)
    file_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
