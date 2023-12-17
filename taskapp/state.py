import json

from asyncpg import Pool, create_pool

import taskapp.conf as conf
from taskapp.repository.session import SessionRepository
from taskapp.repository.task import TaskRepository
from taskapp.repository.user import UserRepository


class AppState:
    def __init__(self) -> None:
        self._db = None
        self._session_repo = None
        self._user_repo = None
        self._task_repo = None

    async def init_connection(self, conn):
        await conn.set_type_codec(
            "jsonb",
            encoder=json.dumps,
            decoder=json.loads,
            schema="pg_catalog",
        )

    async def startup(self) -> None:
        self._db = await create_pool(
            dsn=conf.DATABASE_DSN, init=self.init_connection
        )
        self._session_repo = SessionRepository(db=self.db)
        self._user_repo = UserRepository(db=self.db)
        self._task_repo = TaskRepository(db=self.db)

    async def shutdown(self) -> None:
        if self._db:
            await self._db.close()

    @property
    def db(self) -> Pool:
        assert self._db
        return self._db

    @property
    def session_repo(self) -> SessionRepository:
        assert self._session_repo
        return self._session_repo

    @property
    def user_repo(self) -> UserRepository:
        assert self._user_repo
        return self._user_repo

    @property
    def task_repo(self) -> TaskRepository:
        assert self._task_repo
        return self._task_repo


app_state = AppState()
