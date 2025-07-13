from fastapi import FastAPI, Request
import httpx
import os
import logging
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

app = FastAPI()

# Настройка логгера
logging.basicConfig(level=logging.DEBUG)

@app.post("/")
async def forward_to_make(request: Request):
    try:
        data = await request.json()
        logging.info(f"🔁 Получен запрос: {data}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=data)
            logging.info(f"✅ Ответ от Make: {response.status_code} - {response.text}")
            return JSONResponse(content={"status": "ok", "make_response": response.text})

    except Exception as e:
        logging.exception("❌ Ошибка при отправке в Make")
        return JSONResponse(status_code=500, content={"error": str(e)})
