from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# AES-256 Key (32 bytes)
KEY = b"12345678901234567890123456789012"

def encrypt_data(data: str):
    cipher = AES.new(KEY, AES.MODE_CBC)

    ciphertext = cipher.encrypt(
        pad(data.encode(), AES.block_size)
    )

    return {
        "iv": base64.b64encode(cipher.iv).decode(),
        "data": base64.b64encode(ciphertext).decode()
    }

def decrypt_data(iv, ciphertext):
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)

    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

    return plaintext.decode()