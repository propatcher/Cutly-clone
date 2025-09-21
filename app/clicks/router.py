from fastapi import APIRouter, Depends

from app.clicks.dao import ClicksDAO
from app.exceptions import TokenAbsentException
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/click",
    tags=["Переходы по созданным ссылкам"]
)

@router.get("")
async def get_your_click(current_user: User = Depends(get_current_user)):
    if not User:
        raise TokenAbsentException
    return await ClicksDAO.find_all()