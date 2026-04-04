from datetime import datetime, UTC

from peewee import BooleanField, CharField, DateTimeField, IntegerField, TextField

from app.database import BaseModel


class Link(BaseModel):
    slug = CharField(unique=True, max_length=32)
    target_url = TextField()
    is_active = BooleanField(default=True)
    visit_count = IntegerField(default=0)
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
