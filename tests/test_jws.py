import pytest
from src.accounts_manager import AccountManager
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

    def test_parse_new_order(self):
        jws = JWS(
            protected="eyJhbGciOiAiRVMyNTYiLCAibm9uY2UiOiAia2NnQUR1aHVvdFhtbFF3IiwgInVybCI6ICJodHRwOi8vbG9jYWxob3N0OjUwMDAvYWNtZS9uZXctb3JkZXIiLCAia2lkIjogImh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9hY21lL2FjY3QvU3lndGZMdWhtcVZFbnQvb3JkZXJzIn0",
            payload="eyJpZGVudGlmaWVycyI6IFt7InR5cGUiOiAiZG5zIiwgInZhbHVlIjogImxvY2FsaG9zdCJ9XX0",
            signature="zNb32a8F3kXD7ZtFtBApnC4k6aCzjEWrxyIV2KZ4auHoY3959Lo0wJ37eha0KoQdj2QSbGzEG02mJmHjGZD2Zg",
            checkNonce=False,
            newAccount=False,
            jwk={
                "kty": "EC",
                "crv": "P-256",
                "x": "HATm0cXq3KQVPH7kI08MRcKeLc2U2Qe9dT7Y3H-a-N0",
                "y": "8vHcfO0H557GjX0TxqF5JNOrCFWTxJ4pIvePWb69caQ",
            },
        )

        assert jws.payload["identifiers"][0]["type"] == "dns"
