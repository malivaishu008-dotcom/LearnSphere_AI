import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app as application
from services.gemini_service import GeminiServiceError

# Setup test DB paths
root = Path(__file__).resolve().parents[2]
application.DATABASE = root / 'database' / 'test_quota.db'
application.UPLOADS = root / 'storage' / 'uploads_test'
application.app.config['TESTING'] = True
application.app.config['JWT_SECRET_KEY'] = 'test-secret-with-at-least-32-characters'

# Initialize DB
application.init_db()
client = application.app.test_client()

# Register a user
res = client.post('/api/auth/register', json={'name':'QuotaTest','email':'quota@test.local','password':'Password123!'})
print('register status', res.status_code)
if res.status_code != 201:
    print('register failed', res.get_data(as_text=True))
    raise SystemExit(1)

token = res.get_json().get('token')
headers = {'Authorization': 'Bearer ' + token}

# Patch the service to simulate RESOURCE_EXHAUSTED
import services.gemini_service as gs

def fake_generate(history, message):
    raise GeminiServiceError("Study Coach: Gemini's project quota is exhausted. Wait for the quota reset or update quota/billing in Google AI Studio.", retryable=False, error_code='RESOURCE_EXHAUSTED')

gs.generate_chat_response = fake_generate

# Send a study-coach chat
res = client.post('/api/study-coach/chat', headers=headers, json={'message':'What is a data structure?'})
print('chat status', res.status_code)
print(res.get_json())
