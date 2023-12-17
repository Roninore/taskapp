from enum import StrEnum

from pydantic import BaseModel


class AuthBody(BaseModel):
    """
    Тело запроса за аутентификацией.
    """

    username: str
    password: str


class LogoutStatus(StrEnum):
    ok = "ok"


class LogoutResponse(BaseModel):
    status: LogoutStatus
