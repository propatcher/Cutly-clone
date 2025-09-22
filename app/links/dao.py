from sqlalchemy import delete, insert, select, update
from app.exceptions import TokenAbsentException
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
            
    async def delete_your_links(user_id:int, link_id:int):
        async with async_session() as session:
            query = select(Link).where(Link.id == link_id, Link.user_id == user_id)
            result = await session.execute(query)
            link = result.scalar_one_or_none()
            if not link:
                raise TokenAbsentException("Link not found or access denied")
            delete_query = delete(Link).where(Link.id == link_id)
            result = await session.execute(delete_query)
            await session.commit()
            return result.rowcount
    @classmethod
    async def increment_click_count(cls, link_id: int):
        async with async_session() as session:
            # Используйте cls.model вместо Link для consistency
            query = update(cls.model).where(cls.model.id == link_id).values(
                clicks_count=cls.model.clicks_count + 1
            )
            await session.execute(query)
            await session.commit()