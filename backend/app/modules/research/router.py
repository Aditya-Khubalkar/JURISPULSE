from fastapi import APIRouter
router = APIRouter(prefix="/research", tags=["Research"])
@router.get("/precedents")
async def precedents(): return [{"citation": "(2014) 8 SCC 273", "court": "Supreme Court of India"}]
