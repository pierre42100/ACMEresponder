"""
Accounts manager classes
"""

import os
from pathlib import Path
import json
from src.config import settings
from src.rand_utils import get_random_string


class Account:
    """
    Single account information
    """

    def __init__(self, accid: str, jwk):
        """
        Construct a new account class object
        """
        self.id = accid
        self.jwk = jwk

    def orders_url(self) -> str:
        """
        Get account orders URL
        """
        return f"{settings.domain_uri}/acme/acct/{self.id}/orders"


class AccountManager:
    """
    Accounts manager
    """

    @staticmethod
    def account_path(accId: str) -> Path:
        """
        Get the path to the file containing an account's information
        """
        return Path(os.path.join(settings.storage_path, "accounts", accId))

    @staticmethod
    def createAccount(jwk) -> str:
        """
        Create a new account

        Generates an accounts ID and dumps the account key
        """
        accId = get_random_string(14)

        file_path = AccountManager.account_path(accId)
        file_path.parent.mkdir(exist_ok=True, parents=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(jwk))

        return accId

    @staticmethod
    def existsAccount(accId: str):
        """
        Check out whether an account exists or not
        """
        return AccountManager.account_path(accId).exists()

    @staticmethod
    def getAccount(accId: str) -> Account:
        """
        Get an existing account information
        """
        with open(AccountManager.account_path(accId), "r", encoding="utf-8") as f:
            return Account(accId, json.loads(f.read()))
