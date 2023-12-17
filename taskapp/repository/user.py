import logging
from enum import IntEnum

from asyncpg import Pool
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class UserRole(IntEnum):
    performer = 0
    manager = 1
    admin = 2


class User(BaseModel):
    """
    Пользователь системы.
    """

    id: int
    role: UserRole
    username: str
    full_name: str
    password_encrypted: str


class UserWithoutSecrets(BaseModel):
    id: int
    role: UserRole
    username: str
    full_name: str


class UserRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """
        Получает пользователя по id.
        """
        sql = """
            SELECT *
            FROM "user"
            WHERE "id" = $1
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, user_id)

        if not row:
            return

        return User(**dict(row))

    async def get_by_username(self, username: str) -> User | None:
        """
        Получает пользователя по telegram_id.
        """
        sql = """
            SELECT *
            FROM "user"
            WHERE "username" = $1
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, username)

        if not row:
            return

        return User(**dict(row))

    async def get_users(self) -> list[UserWithoutSecrets]:
        sql = """
            SELECT * FROM "user"
        """
        async with self._db.acquire() as c:
            rows = await c.fetch(sql)
        if not len(rows):
            return []
        users = [UserWithoutSecrets(**dict(row)) for row in rows]
        return users

    async def create(
        self,
        username: str,
        full_name: str,
        password_encrypted: str,
        role: UserRole,
    ) -> User | None:
        """
        Создает пользователя.
        """
        sql = """
            INSERT INTO "user"
            ("username", "full_name", "password_encrypted", "role")
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(
                sql, username, full_name, password_encrypted, role
            )

        if not row:
            return

        return User(**dict(row))

    async def update(
        self,
        user_id: int,
        new_role: UserRole,
        new_name: str,
        new_username: str,
    ):
        sql = """
            UPDATE "user"
            SET "role" = $2, "full_name" = $3, "username" = $4
            WHERE "id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(sql, user_id, new_role, new_name, new_username)

    async def change_password(self, user_id: int, new_password_encrypted: str):
        sql = """
            UPDATE "user"
            SET "password_encrypted" = $2
            WHERE "id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(sql, user_id, new_password_encrypted)

    async def delete(self, user_id: int):
        sql = """
            DELETE FROM "user"
            WHERE "id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(sql, user_id)
