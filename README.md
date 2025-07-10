# FileLock_v1

FileLock_v1 is a Python-based hybrid encryption tool that combines symmetric (Fernet) and asymmetric (RSA) encryption techniques to protect files. It uses RSA to encrypt the Fernet key and AES-GCM with Scrypt to protect the private RSA key using a password.

## Features

- RSA 2048-bit key generation
- Password-protected private key using AES-GCM and Scrypt
- Fernet (symmetric) encryption for files
- RSA (asymmetric) encryption of the Fernet key
- Does not delete original files after encryption or decryption

## Requirements

Install dependencies using pip:

```bash
pip install pycryptodome cryptography
```
## Project Structure
```pgsql

FileLock_v1/
├── keygen.py         # Generates RSA key pair and password
├── encryptor.py      # Encrypts files with Fernet, secures key with RSA
├── decryptor.py      # Decrypts files using password and private key
├── keys/             # Stores password, public key, encrypted private key
└── files/            # Place files to encrypt/decrypt here
```
## Usage
## 1. Generate RSA Keys and Password

Run the key generator to produce a public/private key pair and password:
```bash
python3 keygen.py
```
This will create:

-    keys/password.txt - Randomly generated hex password

-    keys/public.pem - RSA public key

-    keys/private.pem - Encrypted private key (AES-GCM)

## 2. Encrypt Files

Add files to the files/ directory (any type or extension). Then run:
```bash
python3 encryptor.py
```
This will:

-    Generate a Fernet key

-    Encrypt each file in files/

 -   Save encrypted files with .encrypted suffix

-    Store the RSA-encrypted Fernet key in encrypted_key.bin

-    Keep original files untouched
### 3. Decrypt Files

To decrypt the .encrypted files, run:
```bash
python3 decryptor.py
```

You will be prompted to enter the password (found in keys/password.txt).

This will:

-    Decrypt the RSA private key using AES-GCM and the password

-    Decrypt the Fernet key from encrypted_key.bin

-    Decrypt all .encrypted files in files/

-    Save the decrypted versions with their original filenames

-    Retain the .encrypted files
## Notes

-    Files are not deleted during encryption or decryption

-    Passwords are stored in plaintext (hex) for simplicity; secure appropriately in practice

-    Loss of the password or private.pem will prevent file recovery

### License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This project is intended for educational and testing purposes only.
Do not use it for malicious activity or to handle sensitive data in production systems without a proper security audit.
