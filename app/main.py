from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def header_testing():
    return {"fastapi_init" : True}