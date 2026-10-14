from fastapi import APIRouter
router = APIRouter(prefix="/roles", tags=["Roles"])
@router.get("")
async def list_roles(): return [{"name": "Managing Partner"}]
