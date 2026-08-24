import uuid
from pathlib import Path

from flask import current_app, request
from werkzeug.utils import secure_filename


def optional_pdf(kind):
    """Save an optional PDF and return its safe public API URL."""
    uploaded = request.files.get("file")
    if not uploaded or not uploaded.filename:
        return None
    if Path(uploaded.filename).suffix.lower() != ".pdf":
        raise ValueError("Only PDF files can be uploaded")
    folder = Path(current_app.config["UPLOAD_FOLDER"]) / kind
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{secure_filename(uploaded.filename)}"
    uploaded.save(folder / filename)
    return f"/uploads/{kind}/{filename}"
