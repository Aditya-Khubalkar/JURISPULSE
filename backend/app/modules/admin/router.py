from fastapi import APIRouter
router = APIRouter(prefix="/admin", tags=["Admin"])
@router.get("/stats")
async def stats(): return {"tenants": 1, "active_users": 12}
