from src.nonce import consumeNonce, getNewNonce


class TestNonce:
    def test_nonces_are_different(self):
        a = getNewNonce()
        b = getNewNonce()
        assert a != b

    def test_non_existing_nonces(self):
        assert not consumeNonce("bad")

    def test_valid_nonce(self):
        a = getNewNonce()
        assert consumeNonce(a)

    def test_consume_twice_nonces(self):
        a = getNewNonce()
        assert consumeNonce(a)
        assert not consumeNonce(a)
