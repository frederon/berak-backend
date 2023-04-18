# pylint: disable=no-self-argument,no-self-use,broad-except
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from . import utils
from .crypto import elliptic_curve, block_cipher

app = FastAPI()

origins = [
    "*"
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
    return {"message": "Cryptography Tugas 3 API"}

class BlockCipherEncryptRequest(BaseModel):
    plaintext: str
    key: str

    @validator('plaintext')
    def validate_plaintext(cls, plaintext):
        return bytes(plaintext, 'utf-8')
    
    @validator('key')
    def validate_key(cls, key):
        return bytes(key, 'utf-8')


class BlockCipherEncryptResponse(BaseModel):
    ciphertext: str


@app.post("/block_cipher/encrypt", tags=["block_cipher"], response_model=BlockCipherEncryptResponse)
async def block_cipher_encrypt(body: BlockCipherEncryptRequest) -> dict:
    try:
        print(body)
        cipher = block_cipher.BlockCipher(body.key)
        ciphertext = cipher.encrypt(body.plaintext)
        return {
            "ciphertext": ciphertext.decode('utf-8')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


class BlockCipherDecryptRequest(BaseModel):
    ciphertext: str
    key: str

    @validator('ciphertext')
    def validate_ciphertext(cls, ciphertext):
        return bytes(ciphertext, 'utf-8')
    
    @validator('key')
    def validate_key(cls, key):
        return bytes(key, 'utf-8')


class BlockCipherDecryptResponse(BaseModel):
    plaintext: str


@app.post("/block_cipher/decrypt", tags=["block_cipher"], response_model=BlockCipherDecryptResponse)
async def enigma_decrypt(body: BlockCipherDecryptRequest) -> dict:
    try:
        cipher = block_cipher.BlockCipher(body.key)
        plaintext = cipher.decrypt(body.ciphertext)
        return {
            "plaintext": plaintext.decode('utf-8')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

class ECGenerateKeyResponse(BaseModel):
    private_key: str
    public_key: str


@app.get("/elliptic_curve/generate_key", tags=["elliptic_curve"], response_model=ECGenerateKeyResponse)
async def elliptic_curve_generate_key() -> dict:
    try:
        private_key = elliptic_curve.gen_ecdsa_private_key()
        public_key = elliptic_curve.gen_ecdsa_public_key(private_key)
        return {"private_key": private_key, "public_key": public_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e