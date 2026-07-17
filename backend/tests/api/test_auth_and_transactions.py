"""High-value API tests for account security and owned records."""


def register(client, email="one@example.test"):
    return client.post("/api/auth/register", json={"displayName": "Test User", "email": email, "password": "safe-password"})


def token_headers(response):
    return {"Authorization": f"Bearer {response.json['accessToken']}"}


def test_health_endpoint_is_public(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_private_category_requires_a_token(client):
    assert client.get("/api/categories").status_code == 401


def test_user_cannot_read_another_users_transaction(client):
    first = register(client)
    headers = token_headers(first)
    category = client.post("/api/categories", headers=headers, json={"name": "Food", "type": "expense"}).json["category"]
    transaction = client.post("/api/transactions", headers=headers, json={"categoryId": category["id"], "amountMinor": 1250, "type": "expense", "date": "2026-01-12"}).json["transaction"]
    second = register(client, "two@example.test")
    response = client.delete(f"/api/transactions/{transaction['id']}", headers=token_headers(second))
    assert response.status_code == 404
