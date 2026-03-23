from pydantic import BaseModel


class ApiResponse(BaseModel):
    success: bool = True
    message: str | None = None
