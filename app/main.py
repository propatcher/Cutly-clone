from fastapi import FastAPI
from app.users.router import router as router_users
from app.links.router import router as router_links
from app.clicks.router import router as router_clicks

app = FastAPI()

app.include_router(router_users)
app.include_router(router_links)
app.include_router(router_clicks)

@app.get("/")
async def header_testing():
    return {"fastapi_init" : True}