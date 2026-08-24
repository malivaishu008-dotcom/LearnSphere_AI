import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

CODE = Path(__file__).resolve().parents[1] / "06_code"
sys.path.insert(0, str(CODE / "backend"))
import app as application


class AcademicContentAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        application.DATABASE = Path(cls.temp_dir) / "test.db"
        application.UPLOADS = Path(cls.temp_dir) / "uploads"
        application.app.config.update(TESTING=True, JWT_SECRET_KEY="test-secret-with-at-least-32-characters")
        application.init_db()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        client = application.app.test_client()
        email = f"academic-{os.urandom(4).hex()}@learnsphere.test"
        token = client.post("/api/auth/register", json={"name": "Student", "email": email, "password": "Password123!"}).get_json()["token"]
        self.client, self.headers = client, {"Authorization": f"Bearer {token}"}

    def test_academic_content_crud_filter_and_upload(self):
        note = self.client.post("/api/notes", headers=self.headers, json={"title": "Backprop", "subject": "ML", "semester": 6, "topic": "Neural nets"})
        self.assertEqual(note.status_code, 201)
        self.assertEqual(self.client.get("/api/notes?subject=ML", headers=self.headers).get_json()["data"][0]["title"], "Backprop")
        self.assertEqual(self.client.put(f"/api/notes/{note.get_json()['data']['id']}", headers=self.headers, json={"description": "Updated"}).status_code, 200)
        syllabus = self.client.post("/api/syllabus", headers=self.headers, json={"subject_code": "ML601", "subject_name": "ML", "semester": 6, "unit": "1", "unit_title": "Intro", "topics": "Regression"})
        self.assertEqual(syllabus.status_code, 201)
        pyq = self.client.post("/api/pyq", headers=self.headers, json={"subject": "ML", "subject_code": "ML601", "semester": 6, "exam_year": 2025, "exam_type": "Final"})
        self.assertEqual(pyq.status_code, 201)
        timetable = self.client.post("/api/timetable", headers=self.headers, json={"day": "Monday", "subject": "ML", "subject_code": "ML601", "semester": 6, "start_time": "09:00", "end_time": "10:00"})
        self.assertEqual(timetable.status_code, 201)
        upload = self.client.post("/api/pyq/upload", headers=self.headers, data={"file": (io.BytesIO(b"%PDF-1.4"), "exam.pdf")}, content_type="multipart/form-data")
        self.assertEqual(upload.status_code, 201)
        self.assertEqual(self.client.post("/api/timetable", headers=self.headers, json={"day": "Monday", "subject": "ML", "subject_code": "ML601", "start_time": "10:00", "end_time": "09:00"}).status_code, 400)
        self.assertEqual(self.client.delete(f"/api/pyq/{pyq.get_json()['data']['id']}", headers=self.headers).status_code, 200)

