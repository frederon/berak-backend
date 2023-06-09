# pylint: disable=no-self-argument,no-self-use,broad-except
import base64
import re
import json
from bs4 import BeautifulSoup
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from . import utils
from .crypto import elliptic_curve, block_cipher, sha3
import html

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
async def block_cipher_encrypt(plaintext: str = Form(...), key: str = Form(...)) -> dict:
    try:
        print("===== ENCRYPT =====")
        plaintext = bytes(plaintext, 'utf-8')
        key = bytes(key, 'utf-8')
        cipher = block_cipher.BlockCipher(key)
        ciphertext = cipher.encrypt(plaintext)
        print('plaintext', plaintext, len(plaintext))
        print('ciphertext', ciphertext, len(plaintext))
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
async def block_cipher_decrypt(ciphertext: str = Form(...), key: str = Form(...)) -> dict:
    try:
        print("===== DECRYPT ======")
        start_index = ciphertext.find("<body>") + len("<body>")
        end_index = ciphertext.find("</body>")

        body_text = ciphertext[start_index:end_index]

        print("---- CIPHER -----")
        print(ciphertext)

        soup = BeautifulSoup(ciphertext, 'html.parser')
        body_text = soup.body.get_text()
        print("=" * 20)
        print("---- BODY TEXT ----")
        print(body_text)
        print("=" * 20)   

        ciphertext = body_text.encode().decode("unicode_escape").encode("raw_unicode_escape")
        ciphertext = ciphertext.replace(b'\r\n', b'\n')
        print(ciphertext)
        print("=" * 20)
        key = bytes(key, 'utf-8')
        cipher = block_cipher.BlockCipher(key) 
        plaintext = cipher.decrypt(ciphertext)
        print('ciphertext', ciphertext)
        print("=" * 20)
        print('plaintext', plaintext)
        return {
            "plaintext": plaintext.decode('utf-8')
        }
    except Exception as e:
        print(e)
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
async def digital_sign(plaintext: str = Form(...), private_key: str = Form(...)) -> dict:
    try:
        private_key = private_key.rstrip().rstrip('\n')
        private_key = int(private_key, 16)

        sha3_instance = sha3.SHA3(sha3.SHA3Instance.SHA256)

        hex_digits = sha3_instance.digest(plaintext)
        hash_digest = utils.convert_hex_digits_to_int_16(hex_digits)

        signature = elliptic_curve.sign(private_key, hash_digest)

        signature_dict = {
            "r": str(signature.r),
            "s": str(signature.s)
        }
        signature_json = json.dumps(signature_dict)
        signature_base64 = utils.convert_str_to_base64(signature_json)

        plaintext_with_signature = utils.append_signature_to_message(plaintext, signature_base64)

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
async def digital_sign_verify(plaintext: str = Form(...), signature_base64: str = Form(...), public_key: str = Form(...)) -> dict:
    try:
        public_key = public_key.rstrip().rstrip('\n')
        
        # plaintext, signature_base64 = utils.extract_signature_from_message(plaintext_with_signature)

        sha3_instance = sha3.SHA3(sha3.SHA3Instance.SHA256)

        hex_digits = sha3_instance.digest(plaintext)
        hash_digest = utils.convert_hex_digits_to_int_16(hex_digits)

        signature_json = utils.convert_base64_to_str(signature_base64)
        signature_dict = json.loads(signature_json)

        signature = elliptic_curve.Signature(int(signature_dict["r"]), int(signature_dict["s"]))

        verified = elliptic_curve.verify(public_key, signature, hash_digest)

        return {
            "verified": verified
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e)) from e