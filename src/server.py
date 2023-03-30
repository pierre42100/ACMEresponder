"""
Core project code
"""

from fastapi import FastAPI, Request

from src.config import settings
from src.nonce import getNewNonce

app = FastAPI()


@app.middleware("http")
async def nonce_middleware(request: Request, call_next):
    """
    Nonce middleware: handles the processing of nonces
    """
    response = await call_next(request)
    response.headers["Replay-Nonce"] = getNewNonce()
    response.headers["Link"] = f'<{settings.domain_uri}acme/directory>;rel="index"'

    return response


@app.get("/")
def root():
    """
    Basic message
    """
    return {
        "name": "Basic ACME responder",
        "source": "https://github.com/pierre42100/ACMEresponder",
    }


@app.get("/directory")
def directory():
    """
    Get routes paths
    """
    return {
        "keyChange": f"{settings.domain_uri}/acme/key-change",
        "meta": {
            "website": "https://github.com/pierre42100/ACMEresponder",
        },
        "newAccount": f"{settings.domain_uri}/acme/new-acct",
        "newNonce": f"{settings.domain_uri}/acme/new-nonce",
        "newOrder": f"{settings.domain_uri}/acme/new-order",
        "renewalInfo": f"{settings.domain_uri}/get/draft-ietf-acme-ari-00/renewalInfo/",
        "revokeCert": f"{settings.domain_uri}/acme/revoke-cert",
    }


@app.head("/acme/new-nonce")
@app.get("/acme/new-nonce", status_code=204)
def new_nonce():
    """
    Request a new nonce
    """
    pass
