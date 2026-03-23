from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.charity import Charity
from app.models.payment import Payment
from app.models.user import User
from app.schemas.charity import CharityOut, DonationRequest
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/charity", tags=["charity"])
settings = get_settings()


@router.get("", response_model=list[CharityOut])
def list_charities(search: str | None = None, category: str | None = None, db: Session = Depends(get_db)):
    query = select(Charity)
    if search:
        q = f"%{search}%"
        query = query.where(or_(Charity.name.ilike(q), Charity.description.ilike(q)))
    if category:
        query = query.where(Charity.category == category)
    return db.execute(query).scalars().all()


@router.get("/featured", response_model=list[CharityOut])
def featured_charities(db: Session = Depends(get_db)):
    return db.execute(select(Charity).where(Charity.featured == True)).scalars().all()


@router.get("/{charity_id}", response_model=CharityOut)
def charity_detail(charity_id: int, db: Session = Depends(get_db)):
    charity = db.get(Charity, charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")
    return charity


@router.post("/select/{charity_id}")
def select_charity(charity_id: int, charity_percent: int = 10, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if charity_percent < 10 or charity_percent > 100:
        raise HTTPException(status_code=400, detail="Charity percentage must be between 10 and 100")
    charity = db.get(Charity, charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")
    user.selected_charity_id = charity_id
    user.charity_percent = charity_percent
    db.commit()
    return {"success": True, "message": "Charity preference updated"}


@router.post("/donate")
def donate(payload: DonationRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    charity = db.get(Charity, payload.charity_id)
    if not charity:
        raise HTTPException(status_code=404, detail="Charity not found")

    payment = Payment(
        user_id=user.id,
        amount=payload.amount,
        currency="usd",
        status="paid" if settings.allow_mock_payments else "pending",
    )
    db.add(payment)
    db.commit()
    return {"success": True, "message": f"Donation recorded for {charity.name}"}
