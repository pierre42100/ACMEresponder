from multiprocessing import Process
import threading
from fastapi.testclient import TestClient
import pytest
import sewer.client
from sewer.crypto import AcmeKey
import uvicorn
from src.accounts_manager import AccountManager
from src.config import Settings
from src.server import app
import time
import tempfile
from src.config import settings


temp_dir = tempfile.TemporaryDirectory()

settings.domain_uri = "http://localhost:5000"
settings.storage_path = temp_dir.name


client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setUp():
    """Bring a test server up."""
    proc = Process(
        target=uvicorn.run,
        args=(app,),
        kwargs={"host": "127.0.0.1", "port": 5000, "log_level": "info"},
        daemon=True,
    )
    proc.start()
    time.sleep(0.1)  # time for the server to start


class TestServer:
    """
    Main server tests
    """

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

    def test_new_account(self):
        client = sewer.client.Client(
            domain_name="localhost",
            account=sewer.client.AcmeAccount.create("secp256r1"),
            is_new_acct=True,
            ACME_DIRECTORY_URL="http://localhost:5000/directory",
            cert_key=AcmeKey.create("rsa2048"),
        )
        res = client.acme_register()
        assert res.status_code == 201

        id = res.headers["location"].split("acct/")[1].split("/")[0]
        assert AccountManager.existsAccount(id)
