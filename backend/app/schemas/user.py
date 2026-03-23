from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    selected_charity_id: int | None
    charity_percent: int
    created_at: datetime

    model_config = {"from_attributes": True}
