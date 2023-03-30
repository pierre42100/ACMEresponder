from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"name": "Basic ACME responder", "source":"https://github.com/pierre42100/ACMEresponder"} 

