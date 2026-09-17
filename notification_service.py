from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notification Service")

class TaskEvent(BaseModel):
    event: str
    task: dict

"/api/webhooks/task_created"
async def task_created(payload: TaskEvent):
    with open("notifications.log", "a", encoding="utf-8") as f:
        f.write(f"NOTIFY: {payload.task['title']}\n")
    return {"status": "received"}