"""Environment-backed Flask configuration."""
import os


class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "replace-this-dev-secret-before-production")
    MAX_CONTENT_LENGTH = 25 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5000,http://127.0.0.1:5000")
    PORT = int(os.getenv("PORT", "5000"))
