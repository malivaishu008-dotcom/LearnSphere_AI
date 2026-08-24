"""SQLAlchemy models for LearnSphere academic content."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.note import Note  # noqa: E402,F401
from models.pyq import PYQ  # noqa: E402,F401
from models.syllabus import Syllabus  # noqa: E402,F401
from models.timetable import Timetable  # noqa: E402,F401
from models.user import User  # noqa: E402,F401
