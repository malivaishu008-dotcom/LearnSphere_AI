from models import db
from models.base import SerializableMixin, utcnow


class User(SerializableMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
