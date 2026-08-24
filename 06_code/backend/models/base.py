from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


class SerializableMixin:
    """Keeps API serialization consistent and explicit."""

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = value.isoformat() if hasattr(value, "isoformat") else value
        return result
