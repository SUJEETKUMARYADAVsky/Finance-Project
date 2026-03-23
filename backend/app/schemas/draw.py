from datetime import datetime
from pydantic import BaseModel


class DrawRunRequest(BaseModel):
    logic_type: str = "random"
    simulation: bool = False


class DrawOut(BaseModel):
    id: int
    month_key: str
    draw_numbers_csv: str
    logic_used: str
    simulation: bool
    jackpot_rollover_amount: float
    total_prize_pool: float
    created_at: datetime

    model_config = {"from_attributes": True}
