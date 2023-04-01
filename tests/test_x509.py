import pytest
from src.base64_utils import safe_base64_decode
from src.time_utils import parse_unix_time
from src.x509 import X509
import time
from cryptography import x509

FIRST_CRL = safe_base64_decode(
    "MIICgDCCAWgCAQAwFDESMBAGA1UEAwwJbG9jYWxob3N0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoMw6mnodn-tHmbyfTSaE34KcUnEHo4p7JE4QAQmfnoMoNb2TgG7gVx5SZOL5fUkLk1Gn6jtrddEdxWjqI4adYuD2gj9jqFDZYbrGoxGPH3ONBOHZ7XSFsRIL75GA8TfF7L-_jAhc2KfZzRRi3ug2-r-74sy8p1VyAyL2iK-XFBFS7B1IwtlScEHP9ni4CRm1tIJn7eWPhFHD0E68hxnNlTfpM3uwF6_SuiIJKnou_uDptwGEqnYTFca_OXCLgnWHrNpPBc5frCzYXKnsjOoLNqZdyJ4x2gUcSnegGwDM-Lms-E4CnHRvtA8wH2n-YgI4Uf1jJdozl-3mUGmyzE7GDwIDAQABoCcwJQYJKoZIhvcNAQkOMRgwFjAUBgNVHREEDTALgglsb2NhbGhvc3QwDQYJKoZIhvcNAQELBQADggEBAIRbBxUGkP4vsTSeZLMF6kCYV1wYE2WFtTngmGE1BC4BUH3mwRWhLx9QXUCd-oXOg5f1cJUV_xJWvFG42MQusyjz7a2HFF75R54AUfyQhfwSAWKA7y70rV71P8MJn__hB90w71szf3j8HHe5-JWcGcMlOUdBOuhgNJqvyhH5zb_JVmU1tqmlX7TAy5Nt23WqpLtdjRVWWLl446AXP-89PbHTNetT9D7juFcDQL_w1wnvFkkOtDcXyBtUPLI8Koe8Kza5LsSesPIsnH2_zMaTeRnhrwePlGTTlLLVphCKVK63B73FTTnkfN_fofmuWeCrnEawLtpaDIQj6pO83gJraLc"
)

ca_pubkey, ca_privkey = X509.generate_selfsigned_cert(hostname="yolo")


class TestValidateCRL:
    """
    X509 CRL tests
    """

    def test_check_crl_valid(self):
        X509.check_crl(FIRST_CRL, ["localhost"])

    def test_check_crl_invalid_hostname(self):
        with pytest.raises(Exception):
            X509.check_crl(FIRST_CRL, ["google.fr"])

    def test_check_crl_random_input(self):
        with pytest.raises(Exception):
            X509.check_crl(b"randm", ["test"])


class TestSignCRL:
    """
    X509 certificate signature test
    """

    def test_sign_valid(self):
        not_before = time.time()
        not_after = time.time() + 3600

        cert_bytes = X509.sign_crl(
            ca_privkey=ca_privkey,
            ca_pubkey=ca_pubkey,
            csr=FIRST_CRL,
            domains=["google.fr", "microsoft.com", "apple.com"],
            not_before=not_before,
            not_after=not_after,
        )
        
        cert = x509.load_pem_x509_certificate(cert_bytes)
        ca_pubkey_parsed = x509.load_pem_x509_certificate(ca_pubkey)

        assert cert.not_valid_before == parse_unix_time(not_before)
        assert cert.not_valid_after == parse_unix_time(not_after)
        cert.verify_directly_issued_by(ca_pubkey_parsed)

