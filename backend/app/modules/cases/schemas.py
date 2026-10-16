from pydantic import BaseModel
class CaseResponse(BaseModel):
    id: str; cnr_number: str; title: str; court_name: str; status: str
