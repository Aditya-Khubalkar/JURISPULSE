import hashlib, secrets
def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${key.hex()}"
def verify_password(plain: str, hashed: str) -> bool:
    try:
        salt, key = hashed.split('$')
        new_k = hashlib.pbkdf2_hmac('sha256', plain.encode(), salt.encode(), 100000)
        return secrets.compare_digest(key, new_k.hex())
    except Exception: return False
