from fastapi import APIRouter
router = APIRouter(prefix="/timeline", tags=["Timeline"])
@router.get("/{cid}")
async def timeline(cid: str): return [{"id": "t-1", "title": "Notice Issued"}]
