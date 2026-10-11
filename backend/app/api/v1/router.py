from fastapi import APIRouter
from backend.app.api.router import api_router
v1_router = APIRouter()
v1_router.include_router(api_router)
