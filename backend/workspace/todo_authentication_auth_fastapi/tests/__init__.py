from unittest import TestCase
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestBase(TestCase):
    def setUp(self):
        self.client = client

    def tearDown(self):
        pass

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_404(self):
        response = self.client.get("/non-existent-route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Not Found"})