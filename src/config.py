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

    def ca_keyfile(self) -> Path:
        """
        Get CA key file
        """
        return Path(os.path.join(self.storage_path, "ca-privkey.pem"))

    def ca_certfile(self) -> Path:
        """
        Get CA certificate
        """
        return Path(os.path.join(self.storage_path, "ca-pubkey.pem"))


settings = Settings()
