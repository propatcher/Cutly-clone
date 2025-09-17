from sqlalchemy import insert
from app.links.models import Link
from app.dao.base_dao import BaseDAO
from app.database import async_session

class LinksDAO(BaseDAO):
    model = Link
    
    @classmethod
    async def add_link(cls, short_code,original_url,user_id):
        async with async_session() as session:
            query = insert(cls.model).values(short_code=short_code,original_url=original_url,user_id=user_id)
            await session.execute(query)
            await session.commit()