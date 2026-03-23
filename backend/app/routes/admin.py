from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.admin_log import AdminLog
from app.models.charity import Charity
from app.models.draw import Draw
from app.models.payment import Payment
from app.models.subscription import Subscription
from app.models.user import User
from app.models.winning import PaymentStatus, ProofStatus, Winning
from app.schemas.admin import MarkPayoutRequest, VerifyWinningRequest
from app.schemas.charity import CharityCreateRequest, CharityOut, CharityUpdateRequest
from app.schemas.draw import DrawOut, DrawRunRequest
from app.schemas.user import UserOut
from app.services.draw_engine import run_monthly_draw
from app.utils.dependencies import require_admin


router = APIRouter(prefix="/admin", tags=["admin"])


def _log(db: Session, admin_user_id: int, action: str, details: str):
    db.add(AdminLog(admin_user_id=admin_user_id, action=action, details=details))


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    users = db.execute(select(User).order_by(desc(User.created_at))).scalars().all()
    return users


@router.post("/run-draw", response_model=DrawOut)
def admin_run_draw(payload: DrawRunRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    if payload.logic_type not in {"random", "frequency-based"}:
        raise HTTPException(status_code=400, detail="logic_type must be random or frequency-based")

    last_real_draw = db.execute(
        select(Draw).where(Draw.simulation == False).order_by(desc(Draw.created_at)).limit(1)
    ).scalar_one_or_none()
    rollover = last_real_draw.jackpot_rollover_amount if last_real_draw else 0.0

    draw = run_monthly_draw(db=db, logic_type=payload.logic_type, simulation=payload.simulation, rollover_amount=rollover)
    _log(db, admin.id, "RUN_DRAW", f"Draw {draw.month_key} via {payload.logic_type}, simulation={payload.simulation}")
    db.commit()
    db.refresh(draw)
    return draw


@router.post("/charity", response_model=CharityOut)
def create_charity(payload: CharityCreateRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    charity = Charity(**payload.model_dump())
    db.add(charity)
    _log(db, admin.id, "CREATE_CHARITY", f"Charity {payload.name}")
    db.commit()
    db.refresh(charity)
    return charity


@router.put("/charity/{charity_id}", response_model=CharityOut)
def update_charity(charity_id: int, payload: CharityUpdateRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    charity = db.get(Charity, charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")

    updates = payload.model_dump(exclude_none=True)
    for key, value in updates.items():
        setattr(charity, key, value)

    _log(db, admin.id, "UPDATE_CHARITY", f"Charity {charity_id}")
    db.commit()
    db.refresh(charity)
    return charity


@router.delete("/charity/{charity_id}")
def delete_charity(charity_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    charity = db.get(Charity, charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")
    db.delete(charity)
    _log(db, admin.id, "DELETE_CHARITY", f"Charity {charity_id}")
    db.commit()
    return {"success": True}


@router.post("/winning/verify")
def verify_winning(payload: VerifyWinningRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    winning = db.get(Winning, payload.winning_id)
    if not winning:
        raise HTTPException(status_code=404, detail="Winning not found")

    if payload.proof_status not in {"pending", "approved", "rejected"}:
        raise HTTPException(status_code=400, detail="Invalid proof status")
    winning.proof_status = ProofStatus(payload.proof_status)
    _log(db, admin.id, "VERIFY_WINNING", f"winning={payload.winning_id}, status={payload.proof_status}")
    db.commit()
    return {"success": True}


@router.post("/winning/payout")
def mark_payout(payload: MarkPayoutRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    winning = db.get(Winning, payload.winning_id)
    if not winning:
        raise HTTPException(status_code=404, detail="Winning not found")

    if payload.payout_status not in {"pending", "paid"}:
        raise HTTPException(status_code=400, detail="Invalid payout status")
    winning.payout_status = PaymentStatus(payload.payout_status)
    _log(db, admin.id, "MARK_PAYOUT", f"winning={payload.winning_id}, status={payload.payout_status}")
    db.commit()
    return {"success": True}


@router.get("/analytics")
def analytics(db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    total_users = db.execute(select(func.count(User.id))).scalar_one()
    total_revenue = db.execute(select(func.coalesce(func.sum(Payment.amount), 0.0))).scalar_one()
    prize_pool = db.execute(select(func.coalesce(func.sum(Draw.total_prize_pool), 0.0))).scalar_one()

    charity_contributions = db.execute(
        select(func.coalesce(func.sum(Payment.amount), 0.0)).where(Payment.status == "paid")
    ).scalar_one()

    return {
        "total_users": total_users,
        "revenue": float(total_revenue),
        "prize_pool": float(prize_pool),
        "charity_contributions": float(charity_contributions),
    }
