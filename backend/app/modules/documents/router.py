from fastapi import APIRouter
router = APIRouter(prefix="/documents", tags=["Documents"])
@router.get("")
async def docs(): return [{"id": "d-1", "title": "Writ Petition Memo", "file_name": "memo.pdf"}]
