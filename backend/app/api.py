# pylint: disable=no-self-argument,no-self-use
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from . import vigenere, utils

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Cryptography Tucil 1 API"}


class VigenereEncryptRequest(BaseModel):
    plaintext: str
    key: str

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return utils.uppercase_and_filter_alphabets(plaintext)

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


class VigenereEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/vigenere/encrypt", tags=["vigenere"], response_model=VigenereEncryptResponse)
async def vigenere_encrypt(body: VigenereEncryptRequest) -> dict:
    try:
        ciphertext = vigenere.encrypt(body.plaintext, body.key)
        return {"ciphertext": ciphertext}
    except Exception as e:
        return {"error": e}


class VigenereDecryptRequest(BaseModel):
    ciphertext: str
    key: str

    @validator('ciphertext')
    def validate_plaintext(cls, ciphertext):
        return utils.uppercase_and_filter_alphabets(ciphertext)

    @validator('key')
    def validate_key(cls, key):
        return utils.uppercase_and_filter_alphabets(key)


class VigenereDecryptResponse(BaseModel):
    plaintext: str


@app.post("/vigenere/decrypt", tags=["vigenere"], response_model=VigenereDecryptResponse)
async def vigenere_decrypt(body: VigenereDecryptRequest) -> dict:
    try:
        plaintext = vigenere.decrypt(body.ciphertext, body.key)
        return {"plaintext": plaintext}
    except Exception as e:
        return {"error": e}
