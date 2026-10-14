from fastapi import APIRouter
router = APIRouter(prefix="/organizations", tags=["Organizations"])
@router.get("/current")
async def get_org(): return {"id": "org-1", "name": "Chambers of Aditya Khubalkar"}
