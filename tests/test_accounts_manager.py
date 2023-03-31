from src.accounts_manager import AccountManager
from src.nonce import consumeNonce, getNewNonce


class TestAccountsManager:
    def test_invalid_account(self):
        assert not AccountManager.existsAccount("bad")

    def test_create_account(self):
        id = AccountManager.createAccount({"data": "one"})
        assert AccountManager.existsAccount(id)
        assert AccountManager.getAccount(id).jwk["data"] == "one"
