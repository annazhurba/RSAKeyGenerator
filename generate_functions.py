from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def generate_key_pair(pin):
    # generating a private key of size 4096
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    # extracting the public key from the private key
    public_key = private_key.public_key()

    # convert the public key to bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # serialize the private key

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # turn pin into bytes
    pin_bytes = bytes(str(pin), 'utf-8')

    # generate a random initialization vector (IV)
    iv = os.urandom(16)

    # pad the pin to the required length
    padded_pin = pin_bytes + b'\0' * (16 - len(pin_bytes) % 16)

    # use AES
    cipher = Cipher(algorithms.AES(padded_pin), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # encrypt the private key bytes
    encrypted_pin = encryptor.update(private_key_bytes) + encryptor.finalize()

    with open('private_key.pem', 'wb') as f1:
        f1.write(encrypted_pin)
    f1.close()

    with open ('public_key.pem', 'wb') as f2:
        f2.write(public_key_bytes)
    f2.close()
