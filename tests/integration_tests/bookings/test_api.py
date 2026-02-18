import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 500),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id":room_id,
            "date_from":date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    res = response.json()
    assert isinstance(res,dict)
    assert res["status"] == "OK"
    assert "data" in res

@pytest.fixture
async def delete_all_bookings(db):
    await db.bookings.delete()
    await db.commit()


 
@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms", [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-02", "2024-08-11", 2),
    (1, "2024-08-03", "2024-08-12", 3),
])
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id":room_id,
            "date_from":date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == 200
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    
    
    
async def test_add_and_get_my_bookings():
    ...