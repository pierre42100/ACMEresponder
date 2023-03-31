"""
Core project code
"""

from fastapi import FastAPI, Request, Response
from src.accounts_manager import AccountManager

from src.config import settings
from src.jws import JWSReq
from src.nonce import NoncesManager

app = FastAPI()


class StartupException(Exception):
    """
    Exception that prevent the server from starting up
    """


if not settings.ca_certfile().exists() or not settings.ca_keyfile().exists():
    raise StartupException("Missing CA information!")


@app.middleware("http")
async def nonce_middleware(request: Request, call_next):
    """
    Nonce middleware: handles the processing of nonces
    """
    response = await call_next(request)
    response.headers["Replay-Nonce"] = NoncesManager.getNewNonce()
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


@app.get("/tos")
def tos():
    """
    Get terms of service
    """
    return "Be cool. Don't try to DOS or hack us. Thanks!"


@app.get("/directory")
def directory():
    """
    Get routes paths
    """
    return {
        "keyChange": f"{settings.domain_uri}/acme/key-change",
        "meta": {
            "website": "https://github.com/pierre42100/ACMEresponder",
            "termsOfService": f"{settings.domain_uri}/tos",
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


@app.post("/acme/new-acct", status_code=201)
def new_account(req: JWSReq, response: Response):
    """
    Register a new account
    """
    jws = req.to_jws(newAccount=True, action="new-acct")
    accountId = AccountManager.createAccount(jws.jwk)
    account = AccountManager.getAccount(accountId)

    response.headers["Location"] = account.orders_url()

    return {
        "status": "valid",
        "contact": [f"mailto:{settings.contact_mail}"],
        "orders": account.orders_url(),
    }
