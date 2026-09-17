import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from .models import db
from .models import Task
from .schemas import TaskIn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("task_service")

NOTIFICATION_URL = "http://localhost:8001/api/webhooks/task_created"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect(reuse_if_open=True)
    db.create_tables([Task])
    yield
    db.close()


app = FastAPI(title="Task Service", lifespan=lifespan)


async def send_webhook(payload: dict) -> None:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(NOTIFICATION_URL, json=payload)
            r.raise_for_status()
            logger.info("Webhook OK: %s", payload["id"])
    except Exception as e:
        logger.warning("Webhook fail (%s): %s", payload["id"], e)


@app.post("/api/tasks", status_code=201)
async def create_task(data: TaskIn):
    task = Task.create(title=data.title, description=data.description)
    payload = task.to_dict()
    await send_webhook(payload)
    return payload