import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "YouthDb")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-change-me")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_client: Any = None
db: Any = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_client, db
    db_client = AsyncIOMotorClient(MONGO_URL)
    db = db_client[MONGO_DB]
    await db.users.create_index("email", unique=True)
    yield
    db_client.close()


app = FastAPI(title="Youth Auth API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


# ── Request / Response models ──────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleAuthRequest(BaseModel):
    code: str
    redirect_uri: str


# ── Helpers ────────────────────────────────────────────────────────

def create_token(user_email: str) -> str:
    payload = {
        "sub": user_email,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def user_response(user: dict) -> dict:
    return {
        "email": user["email"],
        "created_at": user["created_at"].isoformat(),
        "provider": user["provider"],
    }


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        payload = jwt.decode(
            credentials.credentials, JWT_SECRET, algorithms=["HS256"]
        )
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ── POST /users  (register with email + password) ─────────────────

@app.post("/users", status_code=201)
async def register(body: RegisterRequest):
    existing = await db.users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_doc = {
        "email": body.email,
        "password_hash": pwd_context.hash(body.password),
        "provider": "password",
        "created_at": datetime.now(timezone.utc),
    }
    await db.users.insert_one(user_doc)

    token = create_token(body.email)
    return {"token": token, "user": user_response(user_doc)}


# ── GET /users/me  (get current user info) ─────────────────────────

@app.get("/users/me")
async def get_me(user=Depends(get_current_user)):
    return user_response(user)


# ── POST /auth/login  (email + password login) ────────────────────

@app.post("/auth/login")
async def login(body: LoginRequest):
    user = await db.users.find_one({"email": body.email})
    if not user or "password_hash" not in user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_token(user["email"])
    return {"token": token, "user": user_response(user)}


# ── POST /auth/google  (Google OAuth login) ───────────────────────

@app.post("/auth/google")
async def google_auth(body: GoogleAuthRequest):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": body.code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": body.redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        if token_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code")

        access_token = token_resp.json()["access_token"]

        userinfo_resp = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if userinfo_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info")

    google_user = userinfo_resp.json()

    # Upsert: create if new, update provider to google if existing
    now = datetime.now(timezone.utc)
    result = await db.users.find_one_and_update(
        {"email": google_user["email"]},
        {
            "$set": {"provider": "google", "google_id": google_user["id"]},
            "$setOnInsert": {"email": google_user["email"], "created_at": now},
        },
        upsert=True,
        return_document=True,
    )

    token = create_token(google_user["email"])
    return {"token": token, "user": user_response(result)}
