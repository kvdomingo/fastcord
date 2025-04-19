from fastapi import APIRouter
from starlette.responses import RedirectResponse

from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    return RedirectResponse(
        f"https://test.stytch.com/v1/public/oauth/google/start?public_token={settings.STYTCH_PUBLIC_TOKEN}"
    )
