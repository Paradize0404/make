from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

app = FastAPI()

@app.post("/")
async def proxy_to_make(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        await client.post(MAKE_WEBHOOK_URL, json=data)
    return {"status": "forwarded to Make"}
