import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("GEMINI_API_KEY", "test-gemini-api-key")
CODE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06_code"))
sys.path.insert(0, os.path.join(CODE, "backend"))
import app as application


class LearnSphereAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        application.DATABASE = Path(cls.temp_dir) / "test.db"
        application.UPLOADS = Path(cls.temp_dir) / "uploads"
        application.app.config["TESTING"] = True
        application.app.config["JWT_SECRET_KEY"] = "test-secret-with-at-least-32-characters"
        application.init_db()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        self.client = application.app.test_client()
        suffix = os.urandom(4).hex()
        result = self.client.post("/api/auth/register", json={"name": "Test Student", "email": f"student-{suffix}@learnsphere.test", "password": "Password123!"})
        self.assertEqual(result.status_code, 201)
        self.headers = {"Authorization": "Bearer " + result.get_json()["token"]}

    def test_student_can_plan_and_record_learning(self):
        dashboard = self.client.get("/api/dashboard", headers=self.headers)
        self.assertEqual(dashboard.status_code, 200)
        self.assertGreaterEqual(dashboard.get_json()["metrics"]["subjects"], 3)
        task = self.client.post("/api/tasks", headers=self.headers, json={"title": "Test revision", "planned_minutes": 30})
        self.assertEqual(task.status_code, 201)
        note = self.client.post("/api/notes", headers=self.headers, json={"title": "Test note", "body": "Recall beats rereading."})
        self.assertEqual(note.status_code, 201)
        insight = self.client.get("/api/insights", headers=self.headers)
        self.assertEqual(insight.status_code, 200)
        self.assertIn("predicted_mark", insight.get_json())

    @patch("app.generate_chat_response", return_value="Test AI response")
    def test_study_coach_chat_creates_conversation(self, mock_generate_chat_response):
        response = self.client.post("/api/study-coach/chat", headers=self.headers, json={"message": "Explain regression"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["message"]["content"], "Test AI response")
        self.assertIsNotNone(data["conversation_id"])
        mock_generate_chat_response.assert_called_once()

    def test_study_coach_rejects_other_user_conversation(self):
        first = self.client.post("/api/study-coach/conversations", headers=self.headers, json={"title": "Private chat"})
        self.assertEqual(first.status_code, 201)
        conversation_id = first.get_json()["conversation_id"]

        result = self.client.post("/api/auth/register", json={"name": "Second Student", "email": f"second-{os.urandom(4).hex()}@learnsphere.test", "password": "Password123!"})
        second_headers = {"Authorization": "Bearer " + result.get_json()["token"]}
        response = self.client.get(f"/api/study-coach/conversations/{conversation_id}", headers=second_headers)
        self.assertEqual(response.status_code, 404)

    def test_rejects_unauthorized_request(self):
        self.assertEqual(self.client.get("/api/dashboard").status_code, 401)


if __name__ == "__main__":
    unittest.main()
