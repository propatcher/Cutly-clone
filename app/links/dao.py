from sqlalchemy import insert, update
from app.links.models import Link
from app.dao.base_dao import BaseDAO
from app.database import async_session

class LinksDAO(BaseDAO):
    model = Link
    
    @classmethod
    async def add_link(cls, short_code:str,original_url:str,user_id:int):
        async with async_session() as session:
            query = insert(cls.model).values(short_code=short_code,original_url=original_url,user_id=user_id)
            await session.execute(query)
            await session.commit()
    @classmethod
    async def increment_click_count(cls,link_id: int):
        # SQL запрос для увеличения счетчика на 1
        async with async_session() as session:
            query = update(cls.model).where(Link.id == link_id).values(clicks_count=Link.clicks_count + 1)
            await session.execute(query)
            await session.commit()