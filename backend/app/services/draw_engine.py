from collections import Counter
from datetime import datetime
import random
from uuid import uuid4

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.draw import Draw
from app.models.score import Score
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.winning import Winning


def _month_key() -> str:
    return datetime.utcnow().strftime("%Y-%m")


def build_draw_numbers(db: Session, logic_type: str) -> list[int]:
    if logic_type == "frequency-based":
        latest_scores = db.execute(select(Score.value)).all()
        score_values = [row[0] for row in latest_scores]
        if len(score_values) >= 5:
            top = Counter(score_values).most_common(5)
            return sorted([value for value, _ in top])
    return sorted(random.sample(range(1, 46), 5))


def run_monthly_draw(db: Session, logic_type: str, simulation: bool, rollover_amount: float = 0.0) -> Draw:
    month_key = _month_key()
    existing = db.execute(select(Draw).where(Draw.month_key == month_key, Draw.simulation == False)).scalar_one_or_none()
    if existing and not simulation:
        raise ValueError("Monthly draw already executed")

    draw_numbers = build_draw_numbers(db, logic_type)

    active_subs = db.execute(
        select(Subscription)
        .where(Subscription.status == SubscriptionStatus.ACTIVE)
        .order_by(desc(Subscription.started_at))
    ).scalars().all()

    pool = sum(item.amount for item in active_subs) + rollover_amount
    draw = Draw(
        month_key=month_key if not simulation else f"{month_key}-sim-{uuid4().hex[:8]}",
        draw_numbers_csv=",".join(map(str, draw_numbers)),
        logic_used=logic_type,
        simulation=simulation,
        jackpot_rollover_amount=rollover_amount,
        total_prize_pool=pool,
    )
    db.add(draw)
    db.flush()

    if simulation:
        return draw

    eligible_user_ids = {sub.user_id for sub in active_subs if sub.expires_at > datetime.utcnow()}
    winners_by_match: dict[int, list[int]] = {5: [], 4: [], 3: []}

    for user_id in eligible_user_ids:
        user_scores = db.execute(
            select(Score)
            .where(Score.user_id == user_id)
            .order_by(desc(Score.played_at))
            .limit(5)
        ).scalars().all()

        if not user_scores:
            continue

        user_numbers = {score.value for score in user_scores}
        match_count = len(user_numbers.intersection(set(draw_numbers)))
        if match_count in winners_by_match:
            winners_by_match[match_count].append(user_id)

    allocations = {5: 0.40, 4: 0.35, 3: 0.25}

    for match_count, user_ids in winners_by_match.items():
        allocation_amount = pool * allocations[match_count]
        if match_count == 5 and not user_ids:
            draw.jackpot_rollover_amount = draw.jackpot_rollover_amount + allocation_amount
            continue
        if not user_ids:
            continue
        amount_per_user = allocation_amount / len(user_ids)
        for user_id in user_ids:
            db.add(
                Winning(
                    user_id=user_id,
                    draw_id=draw.id,
                    match_count=match_count,
                    amount=amount_per_user,
                )
            )

    return draw
