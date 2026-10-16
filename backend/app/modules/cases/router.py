from fastapi import APIRouter
from typing import List
from .schemas import CaseResponse
router = APIRouter(prefix="/cases", tags=["Cases"])
@router.get("", response_model=List[CaseResponse])
async def list_cases():
    return [{"id": "c-101", "cnr_number": "DHC010045232024", "title": "Rajesh Kumar vs. State", "court_name": "High Court of Delhi", "status": "listed"}]
