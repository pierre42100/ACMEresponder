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

        :param accID: The ID fo the target account
        :return: The path where the information about the account are
            stored
        """
        return Path(os.path.join(settings.storage_path, "accounts", accId))

    @staticmethod
    def createAccount(jwk) -> str:
        """
        Create a new account

        Generates an accounts ID and dumps the account key

        :param jwk: The JWK of the account
        :return: The ID of the created account
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

        :param accId: The ID of the target account
        """
        with open(AccountManager.account_path(accId), "r", encoding="utf-8") as f:
            return Account(accId, json.loads(f.read()))

    @staticmethod
    def getAccountByKid(kid: str) -> Account:
        """
        Get an existing account by its kid. ie by its order URL

        :param kid: The account URL
        """
        return AccountManager.getAccount(kid.split("/acme/acct/")[1].split("/")[0])
