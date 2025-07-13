from fastapi import FastAPI, Request
import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

app = FastAPI()

# Настройка логгера
logging.basicConfig(level=logging.DEBUG)

@app.post("/")
async def proxy_to_make(request: Request):
    data = await request.json()
    logging.info(f"📥 Получен запрос: {data}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(MAKE_WEBHOOK_URL, json=data)
            logging.info(f"📤 Отправлено в Make, статус: {response.status_code}, тело ответа: {response.text}")
    except Exception as e:
        logging.error(f"❌ Ошибка при отправке в Make: {e}")
        return {"status": "error", "details": str(e)}

    return {"status": "forwarded", "make_status": response.status_code}
