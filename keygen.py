#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
import os

def generate_keys():
    os.makedirs('keys', exist_ok=True)
    password = os.urandom(16).hex()

    # Save password
    with open('keys/password.txt', 'w') as f:
        f.write(password)

    # Generate RSA key pair
    key = RSA.generate(2048)
    priv_data = key.export_key()
    pub_data = key.publickey().export_key()

    # Encrypt private key
    salt = os.urandom(16)
    aes_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(priv_data)

    # Save keys
    with open('keys/private.pem', 'wb') as f:
        f.write(salt + cipher.nonce + tag + ct)
    with open('keys/public.pem', 'wb') as f:
        f.write(pub_data)

    print("[✓] RSA keys and password saved in 'keys/'")

if __name__ == "__main__":
    generate_keys()
