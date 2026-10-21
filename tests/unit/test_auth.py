from backend.app.core.security.password import get_password_hash, verify_password
def test_auth():
    h = get_password_hash("test")
    assert verify_password("test", h) is True
