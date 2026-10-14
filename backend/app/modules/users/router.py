from fastapi import APIRouter
from .schemas import UserResponse
router = APIRouter(prefix="/users", tags=["Users"])
@router.get("/me", response_model=UserResponse)
async def me(): return {"id": "u-1", "email": "aditya@jurispulse.law", "full_name": "Adv. Aditya Khubalkar", "role": "partner"}
