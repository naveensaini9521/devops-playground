import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

key = os.urandom(32)
nonce = os.urandom(16)

algorithm = algorithms.ChaCha20(key, nonce)

cipher = Cipher(algorithm, mode=None)

encryptor = cipher.encryptor()

message = b"Hello DevOps"

ciphertext = encryptor.update(message)

print("Encrypted:", ciphertext.hex())

decryptor = Cipher(
    algorithms.ChaCha20(key, nonce),
    mode=None
).decryptor()

plaintext = decryptor.update(ciphertext)

print("Decrypted:", plaintext.decode())