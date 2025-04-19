from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.responses import PlainTextResponse

from app.routers import guilds

app = FastAPI(
    title="Fastcord API",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
)


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


app.include_router(guilds.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
