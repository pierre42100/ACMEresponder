"""
Core project code
"""

from fastapi import FastAPI

from config import settings

app = FastAPI()


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
