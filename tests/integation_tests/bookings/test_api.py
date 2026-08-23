import pytest

from src.api.dependencies import DBDep


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-01", "2026-08-10", 200),
    (1, "2026-08-01", "2026-08-10", 409)
])
async def test_post_booking(
        room_id, date_from, date_to, status_code,
        auth_ac
):

    response = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code

    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["data"]["room_id"] == room_id
        assert res["data"]


@pytest.fixture(scope="module")
async def delete_all_bookings(db_module: DBDep):
    await db_module.bookings.delete()
    await db_module.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count_bookings", [
    (1, "2026-08-01", "2026-08-10", 200, 1),
    (1, "2026-08-01", "2026-08-10", 200, 2),
    (1, "2026-08-01", "2026-08-10", 200, 3)
])
async def test_add_and_get_my_bookings(
        room_id, date_from, date_to, status_code, count_bookings,
        auth_ac, delete_all_bookings
):
    add_booking = await auth_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    add_result = add_booking.json()
    assert add_booking.status_code == status_code
    assert add_result["data"]["room_id"] == room_id
    assert add_result["data"]["date_from"] == date_from
    assert add_result["data"]["date_to"] == date_to
    assert add_result["status_code"] == 200

    get_my_bookings = await auth_ac.get("/bookings/me")

    get_result = get_my_bookings.json()
    print(f"{get_result=}")
    assert get_my_bookings.status_code == 200
    assert len(get_result) == count_bookings