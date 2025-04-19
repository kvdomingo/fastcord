import stytch
from fastapi import HTTPException
from fastapi.security import APIKeyCookie
from starlette import status
from starlette.requests import Request

from app.settings import settings

client = stytch.Client(
    project_id=settings.STYTCH_PROJECT_ID,
    secret=settings.STYTCH_SECRET,
    environment=settings.STYTCH_ENVIRONMENT,
)


class StytchSessionCookie(APIKeyCookie):
    async def __call__(self, request: Request):
        if not (session := request.session.get("stytch_session_jwt")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        res = await client.sessions.authenticate_jwt_async(session_jwt=session)

        if not res.is_success:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return res.session


session_cookie_scheme = StytchSessionCookie(name="session")
