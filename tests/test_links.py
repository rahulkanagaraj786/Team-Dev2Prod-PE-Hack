def test_create_link(client):
    response = client.post(
        "/api/links",
        json={
            "slug": "launch-plan",
            "targetUrl": "https://dev2prod.app/launch",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["slug"] == "launch-plan"


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
