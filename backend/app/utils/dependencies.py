from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionStatus
from app.models.user import User, UserRole


security = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload.get("sub"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication") from exc

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user


def require_active_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    latest_sub = db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(desc(Subscription.started_at))
        .limit(1)
    ).scalar_one_or_none()

    now = datetime.utcnow()
    if not latest_sub or latest_sub.status != SubscriptionStatus.ACTIVE or latest_sub.expires_at <= now:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Active subscription required")

    return current_user
