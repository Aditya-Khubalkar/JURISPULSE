from fastapi import APIRouter
router = APIRouter(prefix="/verification", tags=["Verification"])
@router.get("/status")
async def status(): return {"is_valid": True}
