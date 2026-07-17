from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)
iv = get_random_bytes(16) # iv = initialization vector

message = b"Python Full Stack Developer"

cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(pad(message, AES.block_size))
print("Encrypted:", encrypted.hex())

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
print("Decrypted:", decrypted.decode())