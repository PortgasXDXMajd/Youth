# Youth - Login System

A web application implementing login via **email/password** and **Google OAuth**, built as a technical challenge.

## Tech Stack

- **Backend:** FastAPI (Python) with clean architecture (controller → service → repo)
- **Database:** MongoDB
- **Frontend:** Next.js + React + TypeScript + Tailwind CSS
- **Auth:** Google Identity Platform + JWT
- **Infrastructure:** Docker + Docker Compose

## Quick Start

```bash
./start.sh
```

This builds and starts all services:

| Service        | URL                    | Description          |
|----------------|------------------------|----------------------|
| Frontend       | http://localhost:3000   | Web app              |
| Backend API    | http://localhost:8000   | FastAPI + Swagger     |
| Mongo Express  | http://localhost:8081   | DB admin UI          |
| API Docs       | http://localhost:8000/docs | Swagger UI        |

**Mongo Express login:** `admin@youth.com` / `admin`

## Environment

Google OAuth credentials and JWT secret are included in `backend/.env.dev` for evaluation purposes — this is a technical challenge submission, not a production deployment.

## API Endpoints

All endpoints are versioned under `/api/v1`:

| Method | Endpoint              | Description                  | Rate Limit |
|--------|-----------------------|------------------------------|------------|
| POST   | `/api/v1/auth/register` | Register with email/password | 5/min      |
| POST   | `/api/v1/auth/login`    | Login with email/password    | 10/min     |
| POST   | `/api/v1/auth/google`   | Login with Google OAuth      | 10/min     |
| GET    | `/api/v1/users/me`      | Get current user info        | 30/min     |

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── main.py                 # App entry point
│   │   ├── api/v1.py               # API version router
│   │   ├── core/                   # Config, security, exceptions, rate limiting
│   │   ├── db/                     # MongoDB session (DI via FastAPI Depends)
│   │   ├── logging/                # Rotating file logger
│   │   └── packages/
│   │       ├── auth/               # Auth controller, service, models
│   │       └── users/              # User controller, service, repo, models
│   └── tests/
│       ├── unit/                   # Service logic tests (fake repos)
│       └── integration/            # E2E auth flow tests (mongomock)
├── frontend/
│   └── src/
│       ├── app/                    # Next.js pages
│       ├── components/             # Auth form, user card
│       ├── hooks/                  # useAuth hook
│       ├── lib/                    # HTTP client
│       └── services/               # API service layer
├── docker-compose.yml
└── start.sh
```

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```
