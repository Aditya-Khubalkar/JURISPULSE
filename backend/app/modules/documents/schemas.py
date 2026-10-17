from pydantic import BaseModel
class DocumentResponse(BaseModel): id: str; title: str; file_name: str
