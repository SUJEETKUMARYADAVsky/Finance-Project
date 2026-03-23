from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import get_settings
from app.models.payment import Payment
from app.models.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from app.models.user import User
from app.schemas.subscription import SubscribeRequest, SubscriptionOut
from app.services.stripe_service import StripeService
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/subscription", tags=["subscription"])
settings = get_settings()


@router.post("/subscribe", response_model=SubscriptionOut)
def subscribe(payload: SubscribeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        plan = SubscriptionPlan(payload.plan)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Plan must be monthly or yearly") from exc

    stripe_service = StripeService()
    price = stripe_service.get_plan_price(plan)
    payment_status = "paid" if settings.allow_mock_payments else "pending"
    subscription_status = SubscriptionStatus.ACTIVE if settings.allow_mock_payments else SubscriptionStatus.CANCELLED

    subscription = Subscription(
        user_id=current_user.id,
        plan=plan,
        status=subscription_status,
        amount=price,
        stripe_subscription_id=stripe_service.create_subscription_reference(current_user.id, plan),
        expires_at=stripe_service.get_expiry(plan),
    )
    db.add(subscription)
    db.flush()

    db.add(
        Payment(
            user_id=current_user.id,
            amount=price,
            currency="usd",
            status=payment_status,
        )
    )

    db.commit()
    db.refresh(subscription)
    return subscription


@router.get("/status", response_model=SubscriptionOut | None)
def subscription_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    latest = db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(desc(Subscription.started_at))
        .limit(1)
    ).scalar_one_or_none()

    if not latest:
        return None
    return latest
