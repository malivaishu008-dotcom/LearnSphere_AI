from sqlalchemy import or_

from models import db


class ContentService:
    """Shared persistence operations; routes remain HTTP-focused."""

    def __init__(self, model):
        self.model = model

    def list(self, user_id, filters, search_fields=()):
        query = self.model.query.filter_by(user_id=user_id)
        for field, value in filters.items():
            if value not in (None, "") and hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        term = filters.get("search")
        if term and search_fields:
            query = query.filter(or_(*[getattr(self.model, field).ilike(f"%{term}%") for field in search_fields]))
        return query.order_by(self.model.updated_at.desc() if hasattr(self.model, "updated_at") else self.model.created_at.desc()).all()

    def get(self, record_id, user_id):
        return self.model.query.filter_by(id=record_id, user_id=user_id).first()

    def create(self, user_id, values):
        # Repeated form submissions do not create a second identical record for the same account.
        existing = self.model.query.filter_by(user_id=user_id, **values).first()
        if existing:
            return existing
        record = self.model(user_id=user_id, **values)
        db.session.add(record)
        db.session.commit()
        return record

    def update(self, record, values):
        for key, value in values.items():
            if hasattr(record, key):
                setattr(record, key, value)
        db.session.commit()
        return record

    def delete(self, record):
        db.session.delete(record)
        db.session.commit()
