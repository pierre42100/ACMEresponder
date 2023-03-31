"""
Handling of JWS-encoded payloads
"""

import base64
import json

from jwt import PyJWK

from src.nonce import consumeNonce


def fix_b64_padding(s):
    """
    Fix Base64 padding potential issue
    """
    if len(s) % 4 != 0:
        s += "==="[0 : 4 - (len(s) % 4)]
    return s


class JWS:
    """
    Parse & validate signed data from request
    """

    def __init__(
        self,
        protected: str,
        payload: str,
        signature: str,
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
            raise Exception("Can't have both kid and jwk at the same time!")

        if "kid" in self.protected and newAccount:
            raise Exception("Can't have account ID in new account requests!")

        if "jwk" in self.protected and not newAccount:
            raise Exception("Can't have jwk in non-new account requests!")

        if "nonce" not in self.protected or "url" not in self.protected:
            raise Exception("JWS headers are incomplete!")
        self.url = self.protected["url"]

        if checkNonce and not consumeNonce(self.protected["nonce"]):
            raise Exception("Nonce is invalid!")
        
        if newAccount:
            jwk = self.protected["jwk"]
        else:
            # TODO : get jwk for existing accounts
            raise Exception("existing account authentication unsupported yet!")

        # Check signature
        message = ("%s.%s" % (protected, payload)).encode("utf-8")
        parsed_jwk = PyJWK.from_dict(jwk)
        if not parsed_jwk.Algorithm.verify(message, parsed_jwk.key, self.signature):
            raise Exception("Signature is invalid!")
