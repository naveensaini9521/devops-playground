from cryptography.fernet import Fernet

key = Fernet.generate_key()

cipher = Fernet(key)

message = b"Welcome to Cryptography"

encrypted = cipher.encrypt(message)
print("Encrypted:", encrypted.decode())

decrypted = cipher.decrypt(encrypted)
print("Decrypted:", decrypted.decode())