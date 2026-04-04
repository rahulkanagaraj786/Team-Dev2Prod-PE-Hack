import json

from app.models import Event, Link


def test_create_link_records_created_event(client):
    client.post(
        "/api/links",
        json={
            "slug": "event-created",
            "userId": 4,
            "targetUrl": "https://dev2prod.app/event-created",
        },
    )

    link = Link.get(Link.slug == "event-created")
    event = Event.get(Event.link == link)

    assert event.event_type == "created"
    assert event.user_id == 4
    assert json.loads(event.details) == {
        "original_url": "https://dev2prod.app/event-created",
        "short_code": "event-created",
    }


def test_update_link_records_updated_event(client):
    client.post(
        "/api/links",
        json={
            "slug": "event-updated",
            "targetUrl": "https://dev2prod.app/event-updated",
        },
    )

    client.patch(
        "/api/links/event-updated",
        json={"title": "Updated once"},
    )

    link = Link.get(Link.slug == "event-updated")
    events = list(Event.select().where(Event.link == link).order_by(Event.id))

    assert [event.event_type for event in events] == ["created", "updated"]


def test_resolve_link_records_resolved_event(client):
    client.post(
        "/api/links",
        json={
            "slug": "event-resolved",
            "targetUrl": "https://dev2prod.app/event-resolved",
        },
    )

    client.get("/event-resolved", follow_redirects=False)

    link = Link.get(Link.slug == "event-resolved")
    events = list(Event.select().where(Event.link == link).order_by(Event.id))

    assert [event.event_type for event in events] == ["created", "resolved"]
