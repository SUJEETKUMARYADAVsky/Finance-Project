from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.routes.admin import router as admin_router
from app.routes.auth import router as auth_router
from app.routes.charity import router as charity_router
from app.routes.draw import router as draw_router
from app.routes.scores import router as scores_router
from app.routes.subscription import router as subscription_router
from app.routes.users import router as users_router

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(subscription_router)
app.include_router(scores_router)
app.include_router(draw_router)
app.include_router(charity_router)
app.include_router(admin_router)


@app.get("/")
def health():
    return {"service": settings.app_name, "status": "ok"}
