from sqlalchemy import insert, select, update
from app.clicks.models import Click
from app.links.models import Link
from app.dao.base_dao import BaseDAO
from app.database import async_session

class ClicksDAO(BaseDAO):
    model = Click
    
    @classmethod
    async def add_click(cls, link_id : int, ip_address:str,user_agent:str):
        async with async_session() as session:
            query = insert(cls.model).values(link_id=link_id,ip_address=ip_address,user_agent=user_agent)
            await session.execute(query)
            await session.commit()
    @classmethod
    async def get_user_links_with_clicks_join(cls, user_id: int):
        async with async_session() as session:
            query = (
                select(Link, Click)
                .join(Click, Link.id == Click.link_id, isouter=True)
                .filter(Link.user_id == user_id)
                .order_by(Link.created_at.desc(), Click.clicked_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()
            
