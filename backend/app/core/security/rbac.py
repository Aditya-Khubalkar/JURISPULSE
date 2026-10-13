from fastapi import HTTPException
def check_permission(user_role: str, allowed: list):
    if user_role not in allowed: raise HTTPException(status_code=403, detail="Forbidden")
