import cryptography

from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys


fileName = input("What is the name of the file you would like to encrypt?")


key = Fernet.generate_key()

file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()

file = open('key.key', 'rb')
key = file.read() # The key will be type bytes
file.close()


password_provided = "password" # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once

message = "my deep dark secret".encode()

f = Fernet(key)
encrypted = f.encrypt(message)
print(encrypted)

print("\n\n")

decrypted = f.decrypt(encrypted)
print(decrypted)