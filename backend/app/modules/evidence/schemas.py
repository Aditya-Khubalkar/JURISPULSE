from pydantic import BaseModel
class EvidenceResponse(BaseModel): id: str; title: str; exhibit: str
