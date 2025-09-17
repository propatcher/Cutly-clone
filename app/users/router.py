from fastapi import APIRouter
from app.database import async_session
from app.users.dao import UserDAO

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("")
async def get_all_user_test():
    async with async_session() as session:
        return await UserDAO.find_all()