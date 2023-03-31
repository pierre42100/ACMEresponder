"""
Accounts manager
"""

from src.config import settings
from src.rand_utils import get_random_string
import os
from pathlib import Path
import json


class Account:
    def __init__(self, id: str, jwk):
        self.id = id
        self.jwk = jwk

    def orders_url(self) -> str:
        return f"{settings.domain_uri}/acme/acct/{self.id}/orders"


class AccountManager:
    def account_path(id: str) -> Path:
        """
        Get the path to the file containing an account's information
        """
        return Path(os.path.join(settings.storage_path, "accounts", id))

    def createAccount(jwk) -> str:
        """
        Create a new account

        Generates an accounts ID and dumps the account key
        """
        id = get_random_string(14)

        file_path = AccountManager.account_path(id)
        file_path.parent.mkdir(exist_ok=True, parents=True)

        with open(file_path, "w") as f:
            f.write(json.dumps(jwk))

        return id

    def existsAccount(id):
        """
        Check out whether an account exists or not
        """
        return AccountManager.account_path(id).exists()

    def getAccount(id) -> Account:
        """
        Get an existing account information
        """
        with open(AccountManager.account_path(id), "r") as f:
            return Account(id, json.loads(f.read()))
