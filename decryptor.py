#!/usr/bin/env python3

from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
import os
import getpass
from pathlib import Path

def decrypt_files():
    password = getpass.getpass("Enter password: ")

    # Load and decrypt private key
    with open('keys/private.pem', 'rb') as f:
        data = f.read()
    salt, nonce, tag, ct = data[:16], data[16:32], data[32:48], data[48:]
    aes_key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)
    private_key_bytes = AES.new(aes_key, AES.MODE_GCM, nonce).decrypt_and_verify(ct, tag)
    private_key = RSA.import_key(private_key_bytes)

    # Decrypt symmetric key
    with open('encrypted_key.bin', 'rb') as f:
        enc_key = f.read()
    fernet_key = PKCS1_OAEP.new(private_key).decrypt(enc_key)
    fernet = Fernet(fernet_key)

    # Decrypt files
    for file in Path('files').glob('*.encrypted'):
        data = file.read_bytes()
        decrypted = fernet.decrypt(data)
        original = file.with_suffix('')
        original.write_bytes(decrypted)
        os.remove(file)
        print(f"[✓] Decrypted: {file.name}")

if __name__ == "__main__":
    decrypt_files()
