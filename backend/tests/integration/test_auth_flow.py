def test_register_login_and_get_me(client) -> None:
    # Register
    register_resp = client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "password": "StrongPass123"},
    )
    assert register_resp.status_code == 201
    body = register_resp.json()
    assert body["status"] == 201
    assert body["data"]["email"] == "user1@example.com"
    assert body["data"]["provider"] == "password"

    # Login
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "user1@example.com", "password": "StrongPass123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get me
    me_resp = client.get("/api/v1/users/me", headers=headers)
    assert me_resp.status_code == 200
    me_data = me_resp.json()["data"]
    assert me_data["email"] == "user1@example.com"
    assert me_data["provider"] == "password"


def test_register_duplicate_email(client) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "StrongPass123"},
    )

    resp = client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "password": "StrongPass123"},
    )
    assert resp.status_code == 409
    assert resp.json()["msg"] == "Email already registered"


def test_login_wrong_password(client) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrong@example.com", "password": "StrongPass123"},
    )

    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "WrongPassword"},
    )
    assert resp.status_code == 401
    assert resp.json()["msg"] == "Invalid email or password"


def test_get_me_without_token(client) -> None:
    resp = client.get("/api/v1/users/me")
    assert resp.status_code == 403 or resp.status_code == 401
