def test_create_link(client):
    response = client.post(
        "/api/links",
        json={
            "slug": "launch-plan",
            "userId": 14,
            "targetUrl": "https://dev2prod.app/launch",
            "title": "Launch plan",
        },
    )

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["slug"] == "launch-plan"
    assert data["userId"] == 14
    assert data["title"] == "Launch plan"


def test_list_links_returns_created_items(client):
    client.post(
        "/api/links",
        json={
            "slug": "runbook",
            "targetUrl": "https://dev2prod.app/runbook",
        },
    )

    response = client.get("/api/links")

    assert response.status_code == 200
    assert len(response.get_json()["data"]["links"]) == 1


def test_get_link_returns_one_item(client):
    client.post(
        "/api/links",
        json={
            "slug": "ops-review",
            "userId": 8,
            "targetUrl": "https://dev2prod.app/review",
            "title": "Ops review",
        },
    )

    response = client.get("/api/links/ops-review")

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["slug"] == "ops-review"
    assert data["userId"] == 8
    assert data["title"] == "Ops review"


def test_create_link_rejects_invalid_urls(client):
    response = client.post(
        "/api/links",
        json={
            "slug": "bad-link",
            "targetUrl": "file://not-allowed",
        },
    )

    assert response.status_code == 422
    assert response.get_json()["error"]["message"] == "Use a full http or https URL."


def test_create_link_rejects_invalid_user_id(client):
    response = client.post(
        "/api/links",
        json={
            "slug": "bad-user",
            "userId": 0,
            "targetUrl": "https://dev2prod.app/invalid",
        },
    )

    assert response.status_code == 422
    assert response.get_json()["error"]["message"] == "User ID must be a positive number."
