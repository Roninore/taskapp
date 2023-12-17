import logging
import os

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from fastapi.responses import HTMLResponse

import taskapp.conf as conf
from taskapp.repository.session import Session
from taskapp.state import app_state

from .helpers import check_session, get_password_hash
from .models import AuthBody, LogoutResponse, LogoutStatus

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/_internal_/forbidden_page/index.html")
async def auth_page():
    """
    Возвращает стандартную страницу аутентификации.
    """
    path = os.path.join(conf.STATIC_DIR, "auth_page.html")
    with open(path) as f:
        content = f.read()
    return HTMLResponse(content=content)


@router.post("/_internal_/api/auth")
async def auth(
    body: AuthBody,
    response: Response,
    user_agent: str | None = Header(default=None),
    x_forwarded_for: str | None = Header(default=None),
):
    """
    Выставляет куку для последующей проверки в подзапросах.
    """

    user = await app_state.user_repo.get_by_username(username=body.username)
    if not user:
        logger.info("User not found, username={%s}", body.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    password_encrypted = get_password_hash(body.password)
    logger.info("hash, %s, %s", user.password_encrypted, password_encrypted)
    if password_encrypted != user.password_encrypted:
        logger.info("Wrong password, username={%s}", body.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0]
        session = await app_state.session_repo.create(
            user_id=user.id,
            user_agent=user_agent,
            ip=client_ip,
        )
    else:
        session = await app_state.session_repo.create(
            user_id=user.id, user_agent=user_agent
        )
    response.set_cookie(key="TGAGS", value=session.id, secure=True)


@router.get("/_internal_/api/check_auth")
async def check_auth(_: Session = Depends(check_session)):
    """
    Метод проверки авторизации запроса.
    Используется на nginx.
    """
    return Response(status_code=200)


@router.post("/_internal_/logout", response_model=LogoutResponse)
async def get_my_tasks(session: Session = Depends(check_session)):
    await app_state.session_repo.disable(session_id=session.id)
    return LogoutResponse(status=LogoutStatus.ok)
