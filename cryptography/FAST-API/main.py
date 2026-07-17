from fastapi import FastAPI
from pydantic import BaseModel
from crypto import encrypt_data, decrypt_data

app = FastAPI()

class RequestData(BaseModel):
    iv: str
    data: str


@app.post("/encrypt")
def encrypt(message: str):
    return encrypt_data(message)


@app.post("/decrypt")
def decrypt(req: RequestData):

    original = decrypt_data(req.iv, req.data)

    return {
        "original": original
    }