from datetime import datetime
from pydantic import BaseModel, Field


class ScoreCreateRequest(BaseModel):
    value: int = Field(ge=1, le=45)


class ScoreOut(BaseModel):
    id: int
    value: int
    played_at: datetime

    model_config = {"from_attributes": True}
