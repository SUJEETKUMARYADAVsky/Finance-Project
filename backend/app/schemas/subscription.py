from datetime import datetime
from pydantic import BaseModel


class SubscribeRequest(BaseModel):
    plan: str


class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    plan: str
    status: str
    amount: float
    started_at: datetime
    expires_at: datetime

    model_config = {"from_attributes": True}
