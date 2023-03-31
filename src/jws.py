"""
Handling of JWS-encoded payloads
"""

import base64
import json

from jwt import PyJWK
from pydantic import BaseModel
from src.accounts_manager import AccountManager
from src.config import settings

from src.nonce import NoncesManager


def fix_b64_padding(s):
    """
    Fix Base64 padding potential issue
    """
    if len(s) % 4 != 0:
        s += "==="[0 : 4 - (len(s) % 4)]
    return s


class JWSException(Exception):
    """
    JWS Exception
    """


class JWS:
    """
    Parse & validate signed data from request
    """

    def __init__(
        self,
        protected: str,
        payload: str,
        signature: str,
        jwk=None,
        newAccount: bool = False,
        checkNonce: bool = True,
    ):
        """
        Initialize a new JWS from a request
        """
        self.protected = json.loads(
            base64.urlsafe_b64decode(fix_b64_padding(protected))
        )
        self.payload = json.loads(base64.urlsafe_b64decode(fix_b64_padding(payload)))
        self.signature = base64.urlsafe_b64decode(fix_b64_padding(signature))

        if "kid" in self.protected and "jwk" in self.protected:
            raise JWSException("Can't have both kid and jwk at the same time!")

        if "kid" in self.protected and newAccount:
            raise JWSException("Can't have account ID in new account requests!")

        if "jwk" in self.protected and not newAccount:
            raise JWSException("Can't have jwk in non-new account requests!")

        if "nonce" not in self.protected or "url" not in self.protected:
            raise JWSException("JWS headers are incomplete!")
        self.url = self.protected["url"]

        if checkNonce and not NoncesManager.consumeNonce(self.protected["nonce"]):
            raise JWSException("Nonce is invalid!")

        if jwk is not None:
            self.jwk = jwk
        elif newAccount:
            self.jwk = self.protected["jwk"]
        else:
            self.kid = self.protected["kid"]
            self.jwk = AccountManager.getAccountByKid(self.kid).jwk

        # Check signature
        message = f"{protected}.{payload}".encode("utf-8")
        parsed_jwk = PyJWK.from_dict(self.jwk)
        if not parsed_jwk.Algorithm.verify(message, parsed_jwk.key, self.signature):
            raise JWSException("Signature is invalid!")


class JWSReq(BaseModel):
    """
    Class that old JWS information included in a request
    """

    protected: str
    payload: str
    signature: str

    def to_jws(
        self,
        newAccount: bool = False,
        checkNonce: bool = True,
        action: str = "new-acct",
    ) -> JWS:
        """
        Parse a JWS included in a request
        """
        jws = JWS(
            protected=self.protected,
            payload=self.payload,
            signature=self.signature,
            newAccount=newAccount,
            checkNonce=checkNonce,
        )

        if f"{settings.domain_uri}/acme/{action}" != jws.url:
            raise JWSException("Provided URL in JWS is invalid!")

        return jws
