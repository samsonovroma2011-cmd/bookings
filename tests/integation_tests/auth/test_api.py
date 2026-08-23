import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("user@example.com", "1234567890", 200),
    ("brr@patapim.com", "abcdef", 200),
    ("user_example.com", "875675", 422),
    ("user@example.com", "1234567890", 409),
    ("client@example.com", None, 422)
])
async def test_register_login_get_me_logout_user(
        email,
        password,
        status_code,
        ac
):
    register_response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == status_code

    if status_code == 200:
        register_json = register_response.json()
        assert register_json["data"]["email"] == email
        assert register_json["status_code"] == 200

        login_response = await ac.post(
            "/auth/login",
            json={
                "email": email,
                "password": password
            }
        )

        assert login_response.status_code == status_code


        login_json = login_response.json()
        assert login_json["access_token"]
        assert ac.cookies["access_token"]

        get_me_response = await ac.get("/auth/me")

        assert get_me_response.status_code == 200


        get_me_json = get_me_response.json()
        assert get_me_json["id"]
        assert get_me_json["email"] == email

        logout_response = await ac.post("/auth/logout")

        assert logout_response.status_code == status_code


        logout_json = logout_response.json()
        assert logout_json["status_code"] == 200

        assert (await ac.get("/auth/me")).status_code == 401
