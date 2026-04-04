from urllib.parse import urlparse

from flask import Blueprint, jsonify, request
from peewee import DoesNotExist
from peewee import IntegrityError

from app.models import Link

links_bp = Blueprint("links", __name__)


def serialize_link(link):
    return {
        "slug": link.slug,
        "userId": link.user_id,
        "targetUrl": link.target_url,
        "title": link.title,
        "isActive": link.is_active,
        "visitCount": link.visit_count,
        "createdAt": link.created_at.isoformat(),
        "updatedAt": link.updated_at.isoformat(),
    }


def validate_payload(payload):
    if not isinstance(payload, dict):
        return "A JSON body is required."

    slug = payload.get("slug")
    target_url = payload.get("targetUrl")

    if not isinstance(slug, str) or not slug.strip():
        return "A slug is required."

    if not isinstance(target_url, str) or not target_url.strip():
        return "A destination URL is required."

    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "Use a full http or https URL."

    user_id = payload.get("userId")
    if user_id is not None and (not isinstance(user_id, int) or user_id <= 0):
        return "User ID must be a positive number."

    title = payload.get("title")
    if title is not None and (not isinstance(title, str) or not title.strip()):
        return "Title must be plain text."

    return None


@links_bp.get("/api/links")
def list_links():
    links = Link.select().order_by(Link.created_at.desc())
    return jsonify(data={"links": [serialize_link(link) for link in links]})


@links_bp.get("/api/links/<slug>")
def get_link(slug):
    try:
        link = Link.get(Link.slug == slug)
    except DoesNotExist:
        return jsonify(error={"message": "We could not find that link."}), 404

    return jsonify(data=serialize_link(link))


@links_bp.post("/api/links")
def create_link():
    payload = request.get_json(silent=True)
    error = validate_payload(payload)
    if error:
        return jsonify(error={"message": error}), 422

    try:
        link = Link.create(
            slug=payload["slug"].strip().lower(),
            user_id=payload.get("userId"),
            target_url=payload["targetUrl"].strip(),
            title=payload.get("title"),
        )
    except IntegrityError:
        return jsonify(error={"message": "This slug is already in use."}), 409

    return jsonify(data=serialize_link(link)), 201
