import secrets
import string
from fastapi import APIRouter, Depends, HTTPException,Request
from fastapi.responses import RedirectResponse

from app.exceptions import IncorrectEmailOrPasswordException, TokenAbsentException, UserAlreadyExistsException
from app.links.models import Link
from app.users.auth import authenticate_user
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.links.dao import LinksDAO
from app.clicks.dao import ClicksDAO

router = APIRouter(
    prefix="/links",
    tags=["Ссылки"]
)

@router.post("/create")
async def create_short_link(link: str,current_user: User = Depends(get_current_user)):
    if not User:
        raise TokenAbsentException
    all_symbols = string.ascii_letters + string.digits
    secure_random_string = ''.join(secrets.choice(all_symbols) for _ in range(10))
    result = await LinksDAO.add_link(secure_random_string,link,current_user.id)
    return await LinksDAO.find_one_or_none(short_code=secure_random_string)

@router.get("/{short_code}")
async def short_redirect(short_code: str,request:Request):
    link = await LinksDAO.find_one_or_none(short_code=short_code)
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent")
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    await ClicksDAO.add_click(link.id,client_ip,user_agent)
    await LinksDAO.increment_click_count(link.id)
    return RedirectResponse(url=link.original_url)

@router.get("")
async def get_your_links(current_user: User = Depends(get_current_user)):
    if not User:
        raise TokenAbsentException
    return await LinksDAO.find_all(user_id = current_user.id)

@router.get("clicks")
async def get_your_clicks(current_user: User = Depends(get_current_user)):
    if not User:
        raise TokenAbsentException
    return await ClicksDAO.get_user_links_with_clicks_join(current_user.id)