"""
Global project configuration
"""

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


settings = Settings()
