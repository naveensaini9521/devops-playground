from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

key = get_random_bytes(32)

cipher = AES.new(key, AES.MODE_EAX)

message = b"Hello Naveen"

ciphertext, tag = cipher.encrypt_and_digest(message)
print("Encrypted:", base64.b64encode(ciphertext).decode())

decrypt_cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
plaintext = decrypt_cipher.decrypt(ciphertext)
print("Decrypted:", plaintext.decode())