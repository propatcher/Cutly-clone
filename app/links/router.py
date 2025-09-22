import secrets
import string
from fastapi import APIRouter, Depends, HTTPException,Request
from fastapi.responses import RedirectResponse

from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from pydantic import AnyUrl
from app.exceptions import TokenAbsentException
from app.users.dependencies import get_current_user
from app.users.models import User
from app.links.dao import LinksDAO
from app.clicks.dao import ClicksDAO

router = APIRouter(
    prefix="/links",
    tags=["Ссылки"]
)

@router.post("/create")
async def create_short_link(link:AnyUrl,current_user: User = Depends(get_current_user)):
    link_str = str(link)
    all_symbols = string.ascii_letters + string.digits
    secure_random_string = ''.join(secrets.choice(all_symbols) for _ in range(10))
    result = await LinksDAO.add_link(secure_random_string,link_str,current_user.id)
    return await LinksDAO.find_one_or_none(short_code=secure_random_string)


@router.get("/{short_code}")
@cache(expire=3600)
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
    return await LinksDAO.find_all(user_id = current_user.id)

@router.delete("/delete/{link_id}")
async def delete_your_link(link_id:int,current_user: User = Depends(get_current_user)):
    await FastAPICache.clear(key=f"user_{current_user.id}_get_your_links")
    return await LinksDAO.delete_your_links(current_user.id,link_id)
    
    