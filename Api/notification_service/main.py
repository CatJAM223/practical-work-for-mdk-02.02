import logging
from fastapi import FastAPI
from typing import List, Dict

from .schemas import TaskPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification_service")

app = FastAPI(title="Notification Service")

received: List[Dict] = []


@app.post("/api/webhooks/task_created")
async def task_created(payload: TaskPayload):
    received.append(payload.model_dump())
    logger.info("Уведомление получено: %s", payload.id)
    return {"status": "received"}


@app.get("/api/notifications")
async def list_notifications():
    return received