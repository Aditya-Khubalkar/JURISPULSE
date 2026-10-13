import base64, json, time, hmac, hashlib
from backend.app.core.config.settings import settings
def create_access_token(sub: str, exp: int = 86400) -> str:
    p = {"sub": sub, "exp": int(time.time()) + exp}
    h = base64.urlsafe_b64encode(json.dumps({"alg":"HS256"}).encode()).decode().rstrip('=')
    payload = base64.urlsafe_b64encode(json.dumps(p).encode()).decode().rstrip('=')
    sig = hmac.new(str(settings.SECRET_KEY).encode(), f"{h}.{payload}".encode(), hashlib.sha256).digest()
    return f"{h}.{payload}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"
def decode_access_token(token: str):
    try:
        p = token.split('.')[1] + '=='
        return json.loads(base64.urlsafe_b64decode(p.encode()).decode())
    except Exception: return None
