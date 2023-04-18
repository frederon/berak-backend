# pylint: disable=no-self-argument,no-self-use,broad-except
import base64
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from . import utils
from .crypto import elliptic_curve, block_cipher, sha3

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
    
class DigitalSignRequest(BaseModel):
    plaintext: str
    private_key: str
    
    @validator('private_key')
    def validate_private_key(cls, private_key):
        return int(private_key, 16)


class DigitalSignResponse(BaseModel):
    plaintext_with_signature: str
    signature: str
    raw_signature: dict


@app.post("/elliptic_curve/sign", tags=["elliptic_curve"], response_model=DigitalSignResponse)
async def digital_sign(body: DigitalSignRequest) -> dict:
    try:
        sha3_instance = sha3.SHA3(sha3.SHA3Instance.SHA256)

        hex_digits = sha3_instance.digest(body.plaintext)
        hash_digest = utils.convert_hex_digits_to_int_16(hex_digits)

        signature = elliptic_curve.sign(body.private_key, hash_digest)

        signature_dict = {
            "r": str(signature.r),
            "s": str(signature.s)
        }
        signature_json = json.dumps(signature_dict)
        signature_base64 = utils.convert_str_to_base64(signature_json)

        plaintext_with_signature = utils.append_signature_to_message(body.plaintext, signature_base64)

        return {
            "plaintext_with_signature": plaintext_with_signature,
            "signature": signature_base64,
            "raw_signature": signature_dict
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    
class DigitalSignVerifyRequest(BaseModel):
    plaintext_with_signature: str
    public_key: str

class DigitalSignVerifyResponse(BaseModel):
    verified: bool


@app.post("/elliptic_curve/verify", tags=["elliptic_curve"], response_model=DigitalSignVerifyResponse)
async def digital_sign_verify(body: DigitalSignVerifyRequest) -> dict:
    try:
        plaintext, signature_base64 = utils.extract_signature_from_message(body.plaintext_with_signature)

        sha3_instance = sha3.SHA3(sha3.SHA3Instance.SHA256)

        hex_digits = sha3_instance.digest(plaintext)
        hash_digest = utils.convert_hex_digits_to_int_16(hex_digits)

        signature_json = utils.convert_base64_to_str(signature_base64)
        signature_dict = json.loads(signature_json)

        signature = elliptic_curve.Signature(int(signature_dict["r"]), int(signature_dict["s"]))

        verified = elliptic_curve.verify(body.public_key, signature, hash_digest)

        return {
            "verified": verified
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e)) from e