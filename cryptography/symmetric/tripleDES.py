from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

key = DES3.adjust_key_parity(b"126651565165156848489164")
iv = b"12345678"

cipher = DES3.new(key, DES3.MODE_CBC, iv)
message = b"Hello Triple DES"

encrypted = cipher.encrypt(pad(message, DES3.block_size))

print("Encrypted:", encrypted.hex())

cipher = DES3.new(key, DES3.MODE_CBC, iv)

decrypted = unpad(cipher.decrypt(encrypted), DES3.block_size)
print("Decrypted:", decrypted.decode())