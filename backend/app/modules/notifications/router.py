from fastapi import APIRouter
router = APIRouter(prefix="/notifications", tags=["Notifications"])
@router.get("")
async def list_notifs(): return [{"id": "n-1", "title": "Hearing tomorrow"}]
