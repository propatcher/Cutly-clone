import secrets
import string
from fastapi import APIRouter, Body, Depends, HTTPException,Request
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
async def create_short_link(link: AnyUrl = Body(..., embed=True),current_user: User = Depends(get_current_user)):
    return await LinksDAO.add_link(str(link),current_user.id)

@router.get("/{short_code}")
@cache(expire=3600)
async def short_redirect(short_code: str,request:Request):
    link = await LinksDAO.find_one_or_none(short_code=short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    await ClicksDAO.add_click(link.id,request.client.host,request.headers.get("user-agent"))
    await LinksDAO.increment_click_count(link.id)
    return RedirectResponse(url=link.original_url)

@router.get("")
async def get_your_links(current_user: User = Depends(get_current_user)):
    return await LinksDAO.find_all(user_id = current_user.id)

@router.delete("/delete/{link_id}")
async def delete_your_link(link_id:int,current_user: User = Depends(get_current_user)):
    await FastAPICache.clear(key=f"user_{current_user.id}_get_your_links")
    return await LinksDAO.delete_your_links(current_user.id,link_id)
    
    