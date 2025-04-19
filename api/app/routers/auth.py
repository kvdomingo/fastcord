from fastapi import APIRouter, HTTPException, Security
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth import client, session_cookie_scheme
from app.schemas.auth import Session
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    return RedirectResponse(
        f"https://test.stytch.com/v1/public/oauth/google/start?public_token={settings.STYTCH_PUBLIC_TOKEN}"
    )


@router.get("/callback")
async def callback(request: Request):
    token = request.query_params.get("token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    res = await client.oauth.authenticate_async(
        token,
        session_duration_minutes=settings.DEFAULT_SESSION_DURATION_MINUTES,
    )
    if not res.is_success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    request.session.update(
        {
            "stytch_session_jwt": res.session_jwt,
            "stytch_session_token": res.session_token,
            "first_name": res.user.name.first_name,
            "last_name": res.user.name.last_name,
            "email": [e.email for e in res.user.emails][0],
            "user_id": res.user.user_id,
        }
    )
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get("/logout")
async def logout(request: Request):
    if not (session := request.session.get("stytch_session_jwt")):
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    await client.sessions.revoke_async(session_jwt=session)
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@router.get(
    "/me",
    dependencies=[Security(session_cookie_scheme)],
    response_model=Session,
)
async def me(request: Request):
    return request.session
