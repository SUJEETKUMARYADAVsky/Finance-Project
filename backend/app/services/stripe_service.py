from datetime import datetime, timedelta

from app.core.config import get_settings
from app.models.subscription import SubscriptionPlan


class StripeService:
    def __init__(self):
        self.settings = get_settings()

    def get_plan_price(self, plan: SubscriptionPlan) -> float:
        if plan == SubscriptionPlan.YEARLY:
            return 99.0
        return 10.0

    def get_expiry(self, plan: SubscriptionPlan) -> datetime:
        if plan == SubscriptionPlan.YEARLY:
            return datetime.utcnow() + timedelta(days=365)
        return datetime.utcnow() + timedelta(days=30)

    def create_subscription_reference(self, user_id: int, plan: SubscriptionPlan) -> str:
        return f"mock_sub_{user_id}_{plan.value}_{int(datetime.utcnow().timestamp())}"
