import json

from app.models import Event


def record_event(link, event_type, details=None):
    payload = None
    if details is not None:
        payload = json.dumps(details, sort_keys=True)

    return Event.create(
        link=link,
        user_id=link.user_id,
        event_type=event_type,
        details=payload,
    )
