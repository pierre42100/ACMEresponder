"""
X509 certificate management
"""


# Part of this code was taken from a GitHub Gist of Simon Davy.
#
# The code related is the following one :
# * method generate_selfsigned_cert
#
# Copyright 2018 Simon Davy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime, timedelta
import ipaddress
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtensionOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from src.time_utils import parse_unix_time


class X509Exception(Exception):
    """
    Exception that occurred during X509 files processing
    """


class X509:
    """
    X509 Certificates managements
    """

    @staticmethod
    def generate_selfsigned_cert(hostname, ip_addresses=None, key=None):
        """
        Generates self signed certificate for a hostname, and optional IP addresses.
        """

        # Generate our key
        if key is None:
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend(),
            )

        name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, hostname)])

        # best practice seem to be to include the hostname in the SAN,
        # which *SHOULD* mean COMMON_NAME is ignored.
        alt_names = [x509.DNSName(hostname)]

        # allow addressing by IP, for when you don't have real DNS
        # (common in most testing scenarios
        if ip_addresses:
            for addr in ip_addresses:
                # openssl wants DNSnames for ips...
                alt_names.append(x509.DNSName(addr))
                # ... whereas golang's crypto/tls is stricter, and needs IPAddresses
                # note: older versions of cryptography do not understand ip_address objects
                alt_names.append(x509.IPAddress(ipaddress.ip_address(addr)))

        san = x509.SubjectAlternativeName(alt_names)

        # path_len=0 means this cert can only sign itself, not other certs.
        basic_contraints = x509.BasicConstraints(ca=True, path_length=0)
        now = datetime.utcnow()
        cert = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + timedelta(days=10 * 365))
            .add_extension(basic_contraints, False)
            .add_extension(san, False)
            .sign(key, hashes.SHA256(), default_backend())
        )
        cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
        key_pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

        return cert_pem, key_pem

    @staticmethod
    def check_csr(csrb: bytes, domains: list[str]):
        """
        Check if a CSR is valid for signature

        Only the CN attribute of the subject is expected
        """
        csr = x509.load_der_x509_csr(csrb)

        if not csr.is_signature_valid:
            raise X509Exception("Signature of CRL file is invalid!")

        subj_domain = csr.subject.rfc4514_string().replace("CN=", "")
        if not subj_domain in domains:
            raise X509Exception("Subject should be one of the domains name!")

        # Check altnames
        altNames = csr.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )

        for altName in list(altNames.value):
            if altName.value not in domains:
                raise X509Exception(f"Invalid alt name found: ${altName.value}")

    @staticmethod
    def sign_csr(
        ca_privkey: bytes,
        ca_pubkey: bytes,
        csr: bytes,
        domains: list[str],
        not_before: bytes,
        not_after: bytes,
    ) -> bytes:
        """
        Sign a CRL with a certification authority
        """
        crl_parsed = x509.load_der_x509_csr(csr)
        ca_privkey_parsed = load_pem_private_key(ca_privkey, password=None)
        ca_pubkey_parsed = x509.load_pem_x509_certificate(ca_pubkey)

        cert = (
            x509.CertificateBuilder()
            .subject_name(crl_parsed.subject)
            .issuer_name(ca_pubkey_parsed.issuer)
            .public_key(ca_pubkey_parsed.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(parse_unix_time(not_before))
            .not_valid_after(parse_unix_time(not_after))
            .add_extension(
                x509.SubjectAlternativeName(
                    list(map(lambda d: x509.DNSName(d), domains))
                ),
                critical=False,
            )
            .add_extension(
                x509.BasicConstraints(ca=False, path_length=None), critical=True
            )
            .sign(ca_privkey_parsed, hashes.SHA256(), default_backend())
        )

        return cert.public_bytes(encoding=serialization.Encoding.PEM)
