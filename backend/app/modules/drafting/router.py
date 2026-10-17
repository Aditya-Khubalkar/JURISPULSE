from fastapi import APIRouter
router = APIRouter(prefix="/drafting", tags=["Drafting"])
@router.post("/bail")
async def bail(accused: str): return {"content": f"Bail draft for {accused}"}
