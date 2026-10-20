def error_response(code: str, message: str):
    return {"success": False, "error": {"code": code, "message": message}}
