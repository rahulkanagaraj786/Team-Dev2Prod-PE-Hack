def test_missing_route_returns_structured_json_error(client):
    response = client.get("/api/missing/route")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": {
            "code": "route_not_found",
            "message": "That route does not exist.",
        }
    }
