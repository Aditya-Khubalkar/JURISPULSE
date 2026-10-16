from fastapi import APIRouter
router = APIRouter(prefix="/evidence", tags=["Evidence"])
@router.get("/{cid}")
async def evidence(cid: str): return [{"id": "e-1", "title": "Sale Deed", "exhibit": "Ex-P1"}]
