from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"name": "Basic ACME responder", "source":"https://github.com/pierre42100/ACMEresponder"} 

