from fastapi import APIRouter
router = APIRouter(prefix="/hearings", tags=["Hearings"])
@router.get("")
async def hearings(): return [{"id": "h-1", "case_id": "c-101", "hearing_date": "2026-10-28"}]
