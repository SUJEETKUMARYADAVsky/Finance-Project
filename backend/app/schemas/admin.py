from pydantic import BaseModel


class VerifyWinningRequest(BaseModel):
    winning_id: int
    proof_status: str


class MarkPayoutRequest(BaseModel):
    winning_id: int
    payout_status: str
