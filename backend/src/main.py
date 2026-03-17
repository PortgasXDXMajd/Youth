import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.api.v1 import router as v1_router
from src.core.audit_context import clear_current_actor, set_current_actor
from src.core.config import get_settings
from src.core.exceptions import register_exception_handlers
from src.core.rate_limit import limiter
from src.core.rate_limit_handler import rate_limit_exceeded_handler
from src.core.response import ResponseModel, build_response
from src.core.security import decode_token
from src.db.session import close_db, connect_db
from src.logging.logger import setup_logging


settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application in %s mode", settings.app_env)
    await connect_db(app.state)
    yield
    await close_db(app.state)
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Youth login system with Google OAuth and email/password authentication.",
    debug=settings.app_debug,
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

register_exception_handlers(app)
app.include_router(v1_router)


@app.middleware("http")
async def audit_actor_middleware(request: Request, call_next):
    actor = "system"
    auth_header = request.headers.get("Authorization", "")
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        if token:
            try:
                payload = decode_token(token, settings)
                actor = str(payload.get("sub") or "system")
            except Exception:
                actor = "system"

    set_current_actor(actor)
    try:
        return await call_next(request)
    finally:
        clear_current_actor()


@app.get("/", response_model=ResponseModel, tags=["Health"], summary="Service info")
async def root() -> ResponseModel:
    return build_response(
        status=status.HTTP_200_OK,
        msg="Service is running",
        data={"name": settings.app_name, "version": "1.0.0"},
    )


@app.get("/health", response_model=ResponseModel, tags=["Health"], summary="Health check")
async def health() -> ResponseModel:
    return build_response(status=status.HTTP_200_OK, msg="Healthy", data={"status": "ok"})
