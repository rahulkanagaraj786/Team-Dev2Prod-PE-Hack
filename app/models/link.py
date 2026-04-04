from datetime import datetime, UTC

from peewee import BooleanField, CharField, DateTimeField, IntegerField, TextField

from app.database import BaseModel


class Link(BaseModel):
    slug = CharField(unique=True, max_length=32)
    user_id = IntegerField(null=True)
    target_url = TextField()
    title = CharField(max_length=160, null=True)
    is_active = BooleanField(default=True)
    visit_count = IntegerField(default=0)
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))
