from pydantic import BaseModel
class HearingResponse(BaseModel): id: str; case_id: str; hearing_date: str
