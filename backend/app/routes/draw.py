from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.draw import Draw
from app.models.winning import Winning
from app.schemas.draw import DrawOut
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/draw", tags=["draw"])


@router.get("/results", response_model=list[DrawOut])
def get_results(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.execute(select(Draw).order_by(desc(Draw.created_at)).limit(12)).scalars().all()


@router.get("/my-winnings")
def my_winnings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    winnings = db.execute(
        select(Winning).where(Winning.user_id == user.id).order_by(desc(Winning.created_at))
    ).scalars().all()
    return winnings


@router.post("/proof/{winning_id}")
def upload_proof(winning_id: int, proof_url: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    winning = db.get(Winning, winning_id)
    if not winning or winning.user_id != user.id:
        return {"success": False, "message": "Winning not found"}
    winning.proof_url = proof_url
    db.commit()
    return {"success": True, "message": "Proof uploaded"}
