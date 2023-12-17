from datetime import datetime
from secrets import token_urlsafe

from asyncpg import Pool
from pydantic import BaseModel

from taskapp.repository.user import UserRole

from . import helpers


class Session(BaseModel):
    id: str
    user_id: int
    user_role: UserRole
    ip: str | None = None
    user_agent: str | None = None
    is_active: bool
    created_timestamp: datetime


class SessionCreate(BaseModel):
    id: str
    user_id: int
    ip: str | None = None
    user_agent: str | None = None
    is_active: bool


class SessionRepository:
    def __init__(self, db: Pool) -> None:
        self._db = db

    async def get(self, _id: str) -> Session | None:
        """
        Получает сессию.
        """
        sql = """
            SELECT "session".*, "user"."role" as "user_role"
            FROM "session"
            LEFT JOIN "user"
                ON "user"."id" = "session"."user_id"
            WHERE "session"."id" = $1
            """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, _id)

        if not row:
            return

        return Session(**dict(row))

    async def create(
        self,
        user_id: str,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> SessionCreate:
        """
        Создает сессию.
        """
        session = SessionCreate(
            id=token_urlsafe(32),
            user_id=user_id,
            ip=ip,
            user_agent=user_agent,
            is_active=True,
        )
        model_sql = helpers.build_model_sql(session)
        sql = f"""
            INSERT INTO "session" ({model_sql.field_names})
            VALUES ({model_sql.placeholders})
        """
        async with self._db.acquire() as c:
            await c.execute(sql, *model_sql.values)

        return session

    async def disable(self, session_id: str):
        sql = """
            UPDATE "session"
            SET "is_active" = false
            WHERE "id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(sql, session_id)
