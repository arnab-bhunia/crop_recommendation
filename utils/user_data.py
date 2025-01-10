import hashlib
import secrets

users = {}

def hash_password(password):
    salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return salt + hashed_password.hex()

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_password = stored_password[32:]
    hashed_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return hashed_password.hex() == stored_password