# Golf Charity Draw Platform

Production-ready full-stack scaffold for:
- Subscription billing (monthly/yearly)
- Stableford score entry (last 5 retained)
- Monthly draw engine with jackpot rollover
- Charity selection + donations
- User and admin dashboards

## Stack
- Frontend: Next.js (App Router, TypeScript, Tailwind)
- Backend: FastAPI + SQLAlchemy
- DB: PostgreSQL (or SQLite for local quick start)
- Auth: JWT + bcrypt
- Payments: Stripe-ready service abstraction

## Project Structure
- `backend/` FastAPI API and core business logic
- `frontend/` Next.js user/admin interface

## Quick Start
### 1) Backend
```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

### 2) Frontend
```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Frontend: `http://localhost:3000`

## Required APIs (implemented)
- `POST /auth/signup`
- `POST /auth/login`
- `GET /users/me`
- `POST /subscription/subscribe`
- `GET /subscription/status`
- `POST /scores`
- `GET /scores`
- `GET /draw/results`
- `POST /admin/run-draw`
- `GET /admin/analytics`
- Charity list/detail/select/donate endpoints
- Admin charity/winner management endpoints

## Roles
- `user`: personal dashboard features
- `admin`: draw execution, charity CRUD, verification, analytics

## Deployment
- Frontend: Vercel (`frontend/`)
- Backend: Render/Railway (`backend/`)
- Database: Supabase/Postgres, set `DATABASE_URL`

## Notes for Production
- Replace mock Stripe references in `backend/app/services/stripe_service.py` with live checkout/webhook flow.
- Add object storage integration (S3/Supabase Storage) for proof uploads.
- Add Alembic migrations before production rollout.
- Enforce HTTPS and secure CORS origins.
 done 