from fastapi import FastAPI
from app.users.router import router as router_users
from app.links.router import router as router_links
from app.clicks.router import router as router_clicks

from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

app = FastAPI()

app.include_router(router_users)
app.include_router(router_links)
app.include_router(router_clicks)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000" #если на реакте влада 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(f"redis://localhost:6379", encoding="utf8", decode_responses=False)
    FastAPICache.init(RedisBackend(redis), prefix="cache")


@app.get("/")
async def header_testing():
    return {"fastapi_init" : True}