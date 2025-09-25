import secrets
import string
from sqlalchemy import delete, insert, select, update
from app.exceptions import LinkAlreadyExistException, LinkNotExistException, TokenAbsentException
from app.links.models import Link
from app.dao.base_dao import BaseDAO
from app.database import async_session


class LinksDAO(BaseDAO):
    model = Link
    
    async def add_link(original_url: str, user_id: int):
        async with async_session() as session:
            find_query = select(Link).where(
                Link.original_url == original_url.strip(),
                Link.user_id == user_id
            )
            find_result = await session.execute(find_query)
            if find_result.first():
                raise LinkAlreadyExistException

            all_symbols = string.ascii_letters + string.digits
            secure_random_string = ''.join(secrets.choice(all_symbols) for _ in range(10))

            query = insert(Link).values(
                short_code=secure_random_string,
                original_url=original_url.strip(),
                user_id=user_id
            ).returning(Link)

            result = await session.execute(query)
            new_link = result.scalar_one()
            await session.commit()
            return new_link
            
    async def delete_your_links(user_id:int, link_id:int):
        async with async_session() as session:
            query = select(Link).where(
                Link.id == link_id, 
                Link.user_id == user_id)
            result = await session.execute(query)
            link = result.scalar_one_or_none()
            if not link:
                raise LinkNotExistException
            delete_query = delete(Link).where(Link.id == link_id)
            result = await session.execute(delete_query)
            await session.commit()
            return result.rowcount
    @classmethod
    async def increment_click_count(cls, link_id: int):
        async with async_session() as session:
            query = update(cls.model).where(cls.model.id == link_id).values(
                clicks_count=cls.model.clicks_count + 1
            )
            await session.execute(query)
            await session.commit()