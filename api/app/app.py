from datetime import timedelta

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse

from app.routers import auth, guilds
from app.settings import settings

app = FastAPI(
    title="Fastcord API",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_middleware(
    SessionMiddleware,
    session_cookie="session",
    secret_key=settings.SECRET_KEY,
    max_age=int(
        timedelta(minutes=settings.DEFAULT_SESSION_DURATION_MINUTES).total_seconds()
    ),
    same_site="strict",
    https_only=settings.IN_PRODUCTION,
)


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


app.include_router(auth.router)
app.include_router(guilds.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
