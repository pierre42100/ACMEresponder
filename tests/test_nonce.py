from src.nonce import NoncesManager


class TestNonce:
    def test_nonces_are_different(self):
        a = NoncesManager.getNewNonce()
        b = NoncesManager.getNewNonce()
        assert a != b

    def test_non_existing_nonces(self):
        assert not NoncesManager.consumeNonce("bad")

    def test_valid_nonce(self):
        a = NoncesManager.getNewNonce()
        assert NoncesManager.consumeNonce(a)

    def test_consume_twice_nonces(self):
        a = NoncesManager.getNewNonce()
        assert NoncesManager.consumeNonce(a)
        assert not NoncesManager.consumeNonce(a)
