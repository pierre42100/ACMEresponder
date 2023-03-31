import pytest
from src.jws import JWS
import base64
import json


class TestJWS:
    def test_parse_new_account_valid(self):
        jws = JWS(
            protected="eyJhbGciOiAiRVMyNTYiLCAibm9uY2UiOiAiSW1hdWJCeXNQRFpTYVFTIiwgInVybCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMDAvYWNtZS9uZXctYWNjdCIsICJqd2siOiB7Imt0eSI6ICJFQyIsICJjcnYiOiAiUC0yNTYiLCAieCI6ICJpYXkxemdDVER3Z2xRTFdfaGQzdlpnQk5TV0hKaVdzWWh3NTFCZExhTXBNIiwgInkiOiAiM1FJMmFHN1RTODJwSGJSVFdPOVlEUzVDZFh3d2pCMWJ4RVlaeFRzOUdKSSJ9fQ",
            payload="eyJ0ZXJtc09mU2VydmljZUFncmVlZCI6IHRydWV9",
            signature="Gpmud-3slBAs4AV0rmoK3JR-zhhs8iUECQqnjI21JiPMVDJ85-l853vZRMMoKRtwPj5rYSTy5XBf3BIHHD-oNQ",
            checkNonce=False,
            newAccount=True,
        )

        assert jws.payload["termsOfServiceAgreed"] == True

    def test_parse_invalid_nonce(self):
        with pytest.raises(Exception):
            JWS(
                protected="eyJhbGciOiAiRVMyNTYiLCAibm9uY2UiOiAiSW1hdWJCeXNQRFpTYVFTIiwgInVybCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMDAvYWNtZS9uZXctYWNjdCIsICJqd2siOiB7Imt0eSI6ICJFQyIsICJjcnYiOiAiUC0yNTYiLCAieCI6ICJpYXkxemdDVER3Z2xRTFdfaGQzdlpnQk5TV0hKaVdzWWh3NTFCZExhTXBNIiwgInkiOiAiM1FJMmFHN1RTODJwSGJSVFdPOVlEUzVDZFh3d2pCMWJ4RVlaeFRzOUdKSSJ9fQ",
                payload="eyJ0ZXJtc09mU2VydmljZUFncmVlZCI6IHRydWV9",
                signature="Gpmud-3slBAs4AV0rmoK3JR-zhhs8iUECQqnjI21JiPMVDJ85-l853vZRMMoKRtwPj5rYSTy5XBf3BIHHD-oNQ",
                checkNonce=True,
                newAccount=True,
            )

    def test_parse_redundant_jwk(self):
        with pytest.raises(Exception):
            JWS(
                protected="eyJhbGciOiAiRVMyNTYiLCAibm9uY2UiOiAiSW1hdWJCeXNQRFpTYVFTIiwgInVybCI6ICJodHRwOi8vbG9jYWxob3N0OjgwMDAvYWNtZS9uZXctYWNjdCIsICJqd2siOiB7Imt0eSI6ICJFQyIsICJjcnYiOiAiUC0yNTYiLCAieCI6ICJpYXkxemdDVER3Z2xRTFdfaGQzdlpnQk5TV0hKaVdzWWh3NTFCZExhTXBNIiwgInkiOiAiM1FJMmFHN1RTODJwSGJSVFdPOVlEUzVDZFh3d2pCMWJ4RVlaeFRzOUdKSSJ9fQ",
                payload="eyJ0ZXJtc09mU2VydmljZUFncmVlZCI6IHRydWV9",
                signature="Gpmud-3slBAs4AV0rmoK3JR-zhhs8iUECQqnjI21JiPMVDJ85-l853vZRMMoKRtwPj5rYSTy5XBf3BIHHD-oNQ",
                checkNonce=False,
                newAccount=False,
            )

    def test_parse_both_jwk_and_kid(self):
        with pytest.raises(Exception):
            JWS(
                protected=base64.urlsafe_b64encode(
                    json.dump(
                        {
                            "kid": "mykid",
                            "jwk": "myjwk",
                            "nonce": "mynonce",
                        }
                    )
                ),
                payload="eyJ0ZXJtc09mU2VydmljZUFncmVlZCI6IHRydWV9",
                signature="Gpmud-3slBAs4AV0rmoK3JR-zhhs8iUECQqnjI21JiPMVDJ85-l853vZRMMoKRtwPj5rYSTy5XBf3BIHHD-oNQ",
            )

    def test_parse_random_data(self):
        with pytest.raises(Exception):
            JWS(protected="hello", payload="world", signature="friend")
