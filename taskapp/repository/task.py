from datetime import datetime
from enum import StrEnum

from asyncpg import Pool
from pydantic import BaseModel

from taskapp.repository.user import User


class TaskState(StrEnum):
    not_started = "not_started"
    in_progress = "in_progress"
    waiting_for_capture = "waiting_for_capture"
    ended = "ended"


class Task(BaseModel):
    id: int
    caption: str
    text: str
    created_by: int
    created_by_name: str | None = None
    state: TaskState
    edited_timestamp: datetime
    created_timestamp: datetime
    performer_id_list: list[int] | None = None
    performer_name_list: list[str] | None = None


class TaskRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def get_by_id(self, task_id: int) -> Task | None:
        sql = """
            SELECT
                "task".*,
                "creator"."full_name" as "created_by_name",
                array_agg("performer"."id") as "performer_id_list",
                array_agg("performer"."full_name") as "performer_name_list"
            FROM "task"
            LEFT JOIN "user" as "creator"
                ON "task"."created_by" = "creator"."id"
            LEFT JOIN "task_performer"
                ON "task"."id" = "task_performer"."task_id"
            LEFT JOIN "user" as "performer"
                ON "task_performer"."user_id" = "performer"."id"
            WHERE "task"."id" = $1
            GROUP BY "task"."id", "creator"."full_name"
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, task_id)

        if not row:
            return

        return Task(**dict(row))

    async def get_task_performers(self, task_id: int) -> list[User]:
        sql = """
            SELECT "user".*
            FROM "task_performer"
            LEFT JOIN "user"
                ON "task_performer"."user_id" = "user"."id"
            WHERE "task_performer"."task_id" = $1
        """
        async with self._db.acquire() as c:
            rows = await c.fetch(sql, task_id)
        if not len(rows):
            return []
        users = [User(**dict(row)) for row in rows]
        return users

    async def get_tasks_by_user(self, user_id: int) -> list[Task]:
        sql = """
            SELECT
                "task".*,
                "creator"."full_name" as "created_by_name",
                array_agg("performer"."id") as "performer_id_list",
                array_agg("performer"."full_name") as "performer_name_list"
            FROM "task"
            LEFT JOIN "user" as "creator"
                ON "task"."created_by" = "creator"."id"
            LEFT JOIN "task_performer"
                ON "task"."id" = "task_performer"."task_id"
            LEFT JOIN "user" as "performer"
                ON "task_performer"."user_id" = "performer"."id"
            WHERE "task_performer"."user_id" = $1
            GROUP BY "task"."id", "creator"."full_name"
        """
        async with self._db.acquire() as c:
            rows = await c.fetch(sql, user_id)
        if not len(rows):
            return []
        tasks = [Task(**dict(row)) for row in rows]
        return tasks

    async def get_tasks(self) -> list[Task]:
        sql = """
            SELECT
                "task".*,
                "creator"."full_name" as "created_by_name",
                array_agg("performer"."id") as "performer_id_list",
                array_agg("performer"."full_name") as "performer_name_list"
            FROM "task"
            LEFT JOIN "user" as "creator"
                ON "task"."created_by" = "creator"."id"
            LEFT JOIN "task_performer"
                ON "task"."id" = "task_performer"."task_id"
            LEFT JOIN "user" as "performer"
                ON "task_performer"."user_id" = "performer"."id"
            GROUP BY "task"."id", "creator"."full_name"
        """
        async with self._db.acquire() as c:
            rows = await c.fetch(sql)
        if not len(rows):
            return []
        tasks = []
        for row in rows:
            row = dict(row)
            performer_id_list = row["performer_id_list"]
            performer_name_list = row["performer_name_list"]

            if not performer_id_list or not performer_id_list[0]:
                row["performer_id_list"] = []
            if not performer_name_list or not performer_name_list[0]:
                row["performer_name_list"] = []
            tasks.append(Task(**dict(row)))
        return tasks

    async def append_performer(self, task_id: int, user_id: int):
        sql = """
            INSERT INTO "task_performer"
            ("task_id", "user_id") VALUES ($1, $2)
            ON CONFLICT ("user_id", "task_id") DO NOTHING
        """
        async with self._db.acquire() as c:
            await c.execute(sql, task_id, user_id)

    async def remove_performer(self, task_id: int, user_id: int):
        sql = """
            DELETE FROM "task_performer"
            WHERE "task_id" = $1 AND "user_id" = $2
        """
        async with self._db.acquire() as c:
            await c.execute(sql, task_id, user_id)

    async def update_state(self, task_id: int, new_state: TaskState):
        sql = """
            UPDATE "task"
            SET state = $2, edited_timestamp = $3
            WHERE "task"."id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(sql, task_id, new_state, datetime.now())

    async def update_task(
        self,
        task_id: int,
        new_caption: str,
        new_text: str,
        new_state: TaskState,
    ):
        sql = """
            UPDATE "task"
            SET caption = $2, text = $3, edited_timestamp = $4, state = $5
            WHERE "task"."id" = $1
        """
        async with self._db.acquire() as c:
            await c.execute(
                sql, task_id, new_caption, new_text, datetime.now(), new_state
            )

    async def create_task(
        self, caption: str, text: str, state: TaskState, created_by: int
    ) -> Task:
        sql = """
            INSERT INTO "task"
            (caption, text, state, created_by)
            VALUES ($1, $2, $3, $4)
            RETURNING *
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, caption, text, state, created_by)
        task = Task(**dict(row))
        return task
