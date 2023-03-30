"""
Core project code
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """
    Basic message
    """
    return {
        "name": "Basic ACME responder",
        "source": "https://github.com/pierre42100/ACMEresponder",
    }
