from datetime import datetime
from sqlalchemy import DateTime, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Draw(Base):
    __tablename__ = "draws"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month_key: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    draw_numbers_csv: Mapped[str] = mapped_column(Text, nullable=False)
    logic_used: Mapped[str] = mapped_column(Text, nullable=False)
    simulation: Mapped[bool] = mapped_column(default=False, nullable=False)
    jackpot_rollover_amount: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    total_prize_pool: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
