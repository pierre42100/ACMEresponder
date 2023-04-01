"""
Global project configuration
"""

import os
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Domain URI for ACME responder

    Overrides with the DOMAIN_URI environment variable
    """

    domain_uri: str = "http://localhost:8000"

    """
    Storage path
    """
    storage_path: str = "storage"

    """
    Contact email
    """
    contact_mail: str = "contact@acme.corp"

    """
    Orders lifetime: the time a client has to fullfill
    the expectation of an order, in seconds
    """
    order_lifetime: int = 60 * 15

    """
    Duration of issued certificates
    """
    certs_duration: int = 3600 * 24 * 30

    """
    The port where the server should connect to on client
    to check for HTTP challenge. This value should never
    have to change.
    """
    http_challenge_port = 80

    def ca_keyfile(self) -> Path:
        """
        Get CA key file
        """
        return Path(os.path.join(self.storage_path, "ca-privkey.pem"))

    def ca_get_keyfile(self) -> bytes:
        """
        Read CA private key
        """
        with open(self.ca_keyfile(), "rb") as f:
            return f.read()

    def ca_certfile(self) -> Path:
        """
        Get CA certificate
        """
        return Path(os.path.join(self.storage_path, "ca-pubkey.pem"))

    def ca_get_certfile(self) -> bytes:
        """
        Read CA certificate
        """
        with open(self.ca_certfile(), "rb") as f:
            return f.read()


settings = Settings()
