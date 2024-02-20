import logging

from asyncpg import Pool
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SegmentationTag(BaseModel):
    id: int
    salebot_tag_id: str


class UserSegmentationTag(BaseModel):
    id: int
    user_id: int
    tag_id: int


class TagRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def get_tag_by_id(self, tag_id) -> SegmentationTag | None:
        """
        Получает тэг из "segmentation_tag" по его id
        """
        sql = """
            SELECT * FROM "segmentation_tag" WHERE id = $1
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, tag_id)

        if not row:
            return

        return SegmentationTag(**dict(row))

    async def add_tag_to_user(self, user_id: int, tag_id: int) -> bool:
        """
        Помещает тэг по пользователю
        """
        sql = """
        INSERT INTO "user_segmentation_tag" ("user_id","tag_id")
            VALUES ($1, $2)
        ON CONFLICT DO NOTHING
        RETURNING *
        """
        async with self._db.acquire() as c:
            data = await c.fetch(sql, user_id, tag_id)
        return bool(data)
