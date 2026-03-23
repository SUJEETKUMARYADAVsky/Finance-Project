from fastapi import APIRouter, Depends
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.score import Score
from app.models.user import User
from app.schemas.score import ScoreCreateRequest, ScoreOut
from app.utils.dependencies import require_active_subscription


router = APIRouter(prefix="/scores", tags=["scores"])


@router.post("", response_model=list[ScoreOut])
def create_score(
    payload: ScoreCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_subscription),
):
    score = Score(user_id=current_user.id, value=payload.value)
    db.add(score)
    db.flush()

    all_scores = db.execute(
        select(Score)
        .where(Score.user_id == current_user.id)
        .order_by(desc(Score.played_at))
    ).scalars().all()

    if len(all_scores) > 5:
        old_scores = all_scores[5:]
        for old in old_scores:
            db.delete(old)

    db.commit()

    latest_five = db.execute(
        select(Score)
        .where(Score.user_id == current_user.id)
        .order_by(desc(Score.played_at))
        .limit(5)
    ).scalars().all()

    return latest_five


@router.get("", response_model=list[ScoreOut])
def get_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_subscription),
):
    return db.execute(
        select(Score)
        .where(Score.user_id == current_user.id)
        .order_by(desc(Score.played_at))
        .limit(5)
    ).scalars().all()
