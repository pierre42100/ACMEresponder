"""
Core project code
"""

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


from src.accounts_manager import AccountManager
from src.config import settings
from src.jws import JWSReq
from src.nonce import NoncesManager
from src.orders_manager import OrdersManager

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class StartupException(Exception):
    """
    Exception that prevent the server from starting up
    """


class RequestException(Exception):
    """
    Exception that occurred during request processing
    """


if not settings.ca_certfile().exists() or not settings.ca_keyfile().exists():
    raise StartupException("Missing CA information!")


@app.middleware("http")
async def nonce_middleware(request: Request, call_next):
    """
    Nonce middleware: handles the processing of nonces

    :param request: The request to process
    :param call_next: Following callback
    """
    response = await call_next(request)
    response.headers["Replay-Nonce"] = NoncesManager.getNewNonce()
    response.headers.append(
        "Link", f'<{settings.domain_uri}/acme/directory>;rel="index"'
    )

    return response


@app.get("/")
def root():
    """
    Basic welcome message
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
    Get ACME routes paths
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
@limiter.limit("100/minute")
def new_nonce(request: Request):
    """
    Request a new nonce

    :param request: Required for the limiter middleware
    """


@app.post("/acme/new-acct", status_code=201)
@limiter.limit("10/minute")
def new_account(req: JWSReq, request: Request, response: Response):
    """
    Register a new account

    :param req: JWS data included in the request
    :param request: Required for the limiter middleware
    :param response: Response object used for headers manipulations
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


@app.post("/acme/new-order", status_code=201)
@limiter.limit("10/minute")
def new_order(req: JWSReq, request: Request, response: Response):
    """
    Start a new order eg. enter in the process of issuing
    a new certificate

    :param req: JWS data included in the request
    :param request: Required for the limiter middleware
    :param response: Response object used for headers manipulations
    """
    jws = req.to_jws(action="new-order")

    if "notBefore" in jws.payload or "notAfter" in jws.payload:
        raise RequestException("notBefore and notAfter are not supported!")

    # Extract requested domains
    entries = []
    for identifier in jws.payload["identifiers"]:
        if identifier["type"] != "dns":
            raise RequestException("Only the 'dns' identifier is supported!")
        entries.append(identifier["value"])

    order = OrdersManager.create(domains=entries, account_id=jws.account_id)
    response.headers["Location"] = order.url()
    return order.info()


@app.post("/acme/authz/{authz_id}")
def authz_status(authz_id: str, req: JWSReq):
    """
    Get the current status of an authorization.

    In this implementation of the ACME server, only the
    authorization for the issuance of DNS certificates
    is supported

    :param authz_id: The Authorization ID
    :param req: JWS data included in the request
    """
    jws = req.to_jws(action=f"authz/{authz_id}")
    authz = OrdersManager.find_domain_by_authz_id(jws.account_id, authz_id=authz_id)

    return authz.info()


@app.post("/acme/chall/{chall_id}")
@limiter.limit("5/minute")
def try_challenge(chall_id: str, request: Request, req: JWSReq, response: Response):
    """
    Attempt to validate a challenge

    :param req: JWS data included in the request
    :param request: Required for the limiter middleware
    :param chall_id: The ID of the challenge to try
    """
    jws = req.to_jws(action=f"chall/{chall_id}")
    authz = OrdersManager.find_domain_by_http_chall_id(
        jws.account_id, chall_id=chall_id
    )

    authz.check_http_challenge(jws.jwk)

    response.headers.append(
        "Link", f'<{settings.domain_uri}/authz/{chall_id}>;rel="up"'
    )

    return authz.info()["challenges"][0]


@app.post("/acme/order/{order_id}/finalize")
@limiter.limit("10/minute")
def finalize_order(order_id: str, req: JWSReq, request: Request, response: Response):
    """
    Submit the CSR to be signed

    :param order_id: The ID of the order to finalize
    :param req: JWS data included in the request
    :param request: Required for the limiter middleware
    :param response: Response object used for manipulations
    """
    jws = req.to_jws(action=f"order/{order_id}/finalize")
    order = OrdersManager.find_order_by_id(jws.account_id, order_id=order_id)

    order.sign_csr(csr=jws.payload["csr"])

    response.headers["Location"] = order.url()
    return order.info()


@app.post("/acme/cert/{cert_id}", response_class=PlainTextResponse)
@limiter.limit("60/minute")
def get_certificate(cert_id: str, req: JWSReq, request: Request, response: Response):
    """
    Retrieve the issued certificate

    :param cert_id: The ID of the certificate to retrieve
    :param req: JWS data included in the request
    :param request: Required for the limiter middleware
    :param response: Response object used for manipulations
    """
    jws = req.to_jws(action=f"cert/{cert_id}")
    order = OrdersManager.find_order_by_cert_id(jws.account_id, cert_id=cert_id)

    chain = f"{order.crt.decode()}{settings.ca_get_certfile().decode()}"

    response.headers["Content-Type"] = "application/pem-certificate-chain"
    return chain
