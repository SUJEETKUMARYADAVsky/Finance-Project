from datetime import datetime
from typing import Optional
import enum
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProofStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"


class Winning(Base):
    __tablename__ = "winnings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    draw_id: Mapped[int] = mapped_column(ForeignKey("draws.id"), nullable=False, index=True)
    match_count: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    proof_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    proof_status: Mapped[ProofStatus] = mapped_column(Enum(ProofStatus), default=ProofStatus.PENDING, nullable=False)
    payout_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="winnings")
