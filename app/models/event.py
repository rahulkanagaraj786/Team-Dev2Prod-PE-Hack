from datetime import datetime, UTC

from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField, TextField

from app.database import BaseModel
from app.models.link import Link


class Event(BaseModel):
    source_id = IntegerField(unique=True, null=True)
    link = ForeignKeyField(Link, backref="events", on_delete="CASCADE")
    user_id = IntegerField(null=True)
    event_type = CharField(max_length=32)
    timestamp = DateTimeField(default=lambda: datetime.now(UTC))
    details = TextField(null=True)
