

async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_facilities_by_title(ac):
    facility_title = "Массаж"
    response = await ac.get("/facilities", params={"title": facility_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, list)
    
