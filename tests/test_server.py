from fastapi.testclient import TestClient

from src.server import app

client = TestClient(app)

class TestServer():
    def test_get_directory(self):
        response = client.get("/directory")
        assert response.status_code == 200

    def test_new_nonce_get(self):
        response = client.get("/acme/new-nonce")
        assert response.status_code == 204
        assert response.headers.get("Replay-Nonce") is not None
    
    def test_new_nonce_head(self):
        response = client.head("/acme/new-nonce")
        assert response.status_code == 200
        assert response.headers.get("Replay-Nonce") is not None
