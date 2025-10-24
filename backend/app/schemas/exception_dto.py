from pydantic import BaseModel
from typing import List, Dict


class BaseExceptionResponse(BaseModel):
    message: str
    errors: List[Dict[str, str]] = []
    success: bool = False


class ValidationErrorResponse(BaseExceptionResponse):
    pass
