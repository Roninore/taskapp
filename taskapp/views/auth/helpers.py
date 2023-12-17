import hashlib
import logging
import re
from datetime import datetime, timedelta

from fastapi import Cookie, Header, HTTPException, status

import taskapp.conf as conf
from taskapp.repository.session import Session
from taskapp.repository.user import UserRole
from taskapp.state import app_state

logger = logging.getLogger(__name__)


def get_password_hash(password: str) -> str:
    hash_object = hashlib.sha256(password.encode())
    encrypted_password = hash_object.hexdigest()
    return encrypted_password


async def check_session(
    TGAGS: str | None = Cookie(default=None),
    x_forwarded_for: str | None = Header(default=None),
) -> Session:
    """
    Зависимость для получения сессии.
    """
    if not TGAGS:
        logger.info("No session cookie.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not x_forwarded_for:
        logger.info("x_forwarded_for is empty")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    client_ip = x_forwarded_for.split(", ")[0]
    if not re.search("10\\.0\\.0\\.\\d{1,3}", client_ip):
        logger.info("%s is not trusted ip", client_ip)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        logger.info("%s is trusted ip", client_ip)

    session = await app_state.session_repo.get(_id=TGAGS)
    if not session:
        logger.info("Session not found.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not session.is_active:
        logger.info("Session not active.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    session_duration = datetime.utcnow() - session.created_timestamp
    if session_duration > timedelta(hours=conf.SESSION_TTL_HOURS):
        logger.info("Session expired.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return session


async def check_manager_session(TGAGS: str | None = Cookie(default=None)):
    session = await check_session(TGAGS=TGAGS)
    if session.user_role < UserRole.manager:
        logger.info("User not a manager")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return session


async def check_admin_session(TGAGS: str | None = Cookie(default=None)):
    session = await check_session(TGAGS=TGAGS)
    if session.user_role < UserRole.admin:
        logger.info("User not a admin")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return session
