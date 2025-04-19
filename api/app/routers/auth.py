from fastapi import APIRouter, Depends, HTTPException, Security
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth import client, session_cookie_scheme
from app.db.generated.models import User
from app.db.generated.users import AsyncQuerier
from app.db.queriers import get_user_async_querier
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
async def login():
    return RedirectResponse(
        f"https://test.stytch.com/v1/public/oauth/google/start?public_token={settings.STYTCH_PUBLIC_TOKEN}"
    )


@router.get("/callback")
async def callback(
    request: Request, querier: AsyncQuerier = Depends(get_user_async_querier)
):
    token = request.query_params.get("token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    res = await client.oauth.authenticate_async(
        token,
        session_duration_minutes=settings.DEFAULT_SESSION_DURATION_MINUTES,
    )
    if not res.is_success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if (user := await querier.get_user(id=res.user.user_id)) is None:
        email = res.user.emails[0].email
        user = await querier.create_user(
            username=email,
            email=email,
            avatar=None,
            cover=None,
        )
        if user is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    request.session.update(
        {
            "stytch": {
                "session_jwt": res.session_jwt,
                "session_token": res.session_token,
            },
            "user": user.model_dump(mode="json"),
        }
    )
    return RedirectResponse(settings.APP_HOST, status_code=status.HTTP_302_FOUND)


@router.get("/logout")
async def logout(request: Request):
    if not (session := request.session.get("stytch_session_jwt")):
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)

    await client.sessions.revoke_async(session_jwt=session)
    request.session.clear()
    return RedirectResponse(settings.APP_HOST, status_code=status.HTTP_302_FOUND)


@router.get(
    "/me",
    dependencies=[Security(session_cookie_scheme)],
    response_model=User,
)
async def me(request: Request):
    return request.session.get("user")
