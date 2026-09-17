from pydantic import BaseModel


class TaskPayload(BaseModel):
    id: str
    title: str
    description: str
    status: str
    created_at: str