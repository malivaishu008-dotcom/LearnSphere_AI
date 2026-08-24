from models import db
from models.base import SerializableMixin, utcnow


class Note(SerializableMixin, db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    subject_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="", nullable=False)
    content = db.Column(db.Text, default="", nullable=False)
    body = db.Column(db.Text, default="", nullable=False)  # legacy frontend compatibility
    file_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
