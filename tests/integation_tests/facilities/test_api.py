from tests.conftest import ac


async def test_post_facility(ac):
    facility_title = "Вид на море"
    response = await ac.post(
        "/facilities",
        json={"title": facility_title}
    )
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res["data"]["title"] == facility_title
    assert res["data"]

async def test_get_facilities(ac):
    get_facilities = await ac.get("/facilities")

    assert get_facilities.status_code == 200
    assert isinstance(get_facilities.json(), list)