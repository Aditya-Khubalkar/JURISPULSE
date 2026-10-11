from fastapi import HTTPException
class JurisPulseException(HTTPException):
    def __init__(self, detail: str, code: int = 400):
        super().__init__(status_code=code, detail=detail)
