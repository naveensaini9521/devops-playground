from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b"12345677"
iv = b"abcdefgh"

cipher = DES.new(key, DES.MODE_CBC, iv)

message = b"Hello DES"

encrypted = cipher.encrypt(pad(message, DES.block_size))
print("Encrypted:", encrypted.hex())

cipher = DES.new(key, DES.MODE_CBC, iv)

decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)

print("Decrypted:", decrypted.decode())