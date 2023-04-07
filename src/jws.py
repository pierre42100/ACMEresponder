"""
Handling of JWS-encoded payloads
"""

import json

from jwt import PyJWK
from pydantic import BaseModel
from src.accounts_manager import AccountManager
from src.base64_utils import safe_base64_decode
from src.config import settings

from src.nonce import NoncesManager


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
        Initialize a new JWS from a request & check it

        :param protected: The protected key of the request
        :param payload: The payload key of the request
        :param signature: The signature of the payload
        :param jwk: The JWK to use to check the signature of the JWS,
            by default either the account
        :param newAccount: Set to true if the JWS if originating from
            a newAccount request
        :param checkNonce: Specify whether the nonce included in the request
            has to be verified or not
        """
        self.protected = json.loads(safe_base64_decode(protected))
        self.payload = (
            None if payload == "" else json.loads(safe_base64_decode(payload))
        )
        self.signature = safe_base64_decode(signature)

        if "kid" in self.protected and "jwk" in self.protected:
            raise JWSException("Can't have both kid and jwk at the same time!")

        if "kid" in self.protected and newAccount:
            raise JWSException("Can't have account ID in new account requests!")

        if "jwk" in self.protected and not newAccount:
            raise JWSException("Can't have jwk in non-new account requests!")

        if "nonce" not in self.protected or "url" not in self.protected:
            raise JWSException("JWS headers are incomplete!")
        self.url = self.protected["url"]

        self.nonce = self.protected["nonce"]
        if checkNonce and not NoncesManager.consumeNonce(self.nonce):
            raise JWSException(f"Nonce '{self.nonce}' is invalid!")

        if jwk is not None:
            self.jwk = jwk
        elif newAccount:
            self.jwk = self.protected["jwk"]
        else:
            self.kid = self.protected["kid"]
            account = AccountManager.getAccountByKid(self.kid)
            self.jwk = account.jwk
            self.account_id = account.id

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
        Parse a JWS included in a request, and construct
        a JWS object from it

        :param newAccount: Set to true if the JWS if originating from
            a newAccount request
        :param checkNonce: Specify whether the nonce included in the JWS
            must be checked
        :param action: The action URI of the request, to control its conformity
            with the one included in the request
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
