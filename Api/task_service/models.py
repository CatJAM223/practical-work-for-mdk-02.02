from peewee import *
import uuid
from datetime import datetime

db = SqliteDatabase('Class_work')

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()))
    title = CharField()
    description = CharField()
    status = CharField(
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
        ],
        default='new',
    )
    created_at = DateTimeField(default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

if __name__ == '__main__':
    db.create_tables(Task)