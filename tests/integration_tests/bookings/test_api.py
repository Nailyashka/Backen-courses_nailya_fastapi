from datetime import datetime
import pytest
import pytest_asyncio

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


# -----------------------------
# Очистка бронирований перед каждым тестом
# -----------------------------
@pytest_asyncio.fixture(autouse=True)
async def clean_bookings(db):
    await db.bookings.delete()
    await db.commit()
    yield


# -----------------------------
# Фикстура: создаем тестовый отель и комнату
@pytest_asyncio.fixture
async def test_room(db):
    hotel = await db.hotels.add(
        HotelAdd(
            title="Test Hotel",
            location="Test Location"
        )
    )

    room = await db.rooms.add(
        RoomAdd(
            hotel_id=hotel.id,
            title="Test Room",
            description="Test Description",
            price=1000,
            quantuty=5
        )
    )

    await db.commit()

    return room


# -----------------------------
# Тест добавления бронирования
# -----------------------------
@pytest.mark.parametrize(
    "date_from, date_to, expected_status",
    [
        ("2024-08-01", "2024-08-10", 200),
        ("2024-08-02", "2024-08-11", 200),
        ("2024-08-03", "2024-08-12", 200),
        ("2024-08-04", "2024-08-13", 200),
        ("2024-08-05", "2024-08-14", 200),
        ("2024-08-17", "2024-08-25", 200),
    ],
)
async def test_add_booking(
    date_from,
    date_to,
    expected_status,
    authenticated_ac,
    test_room,
):
    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": test_room.id,
            "hotel_id": test_room.hotel_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == expected_status

    if response.status_code == 200:
        res = response.json()
        assert res["status"] == "ok"


# -----------------------------
# Тест получения своих бронирований
# -----------------------------
@pytest.mark.parametrize(
    "dates, expected_count",
    [
        (
            [
                ("2024-08-01", "2024-08-10"),
            ],
            1,
        ),
        (
            [
                ("2024-08-01", "2024-08-10"),
                ("2024-08-11", "2024-08-15"),
            ],
            2,
        ),
        (
            [
                ("2024-08-01", "2024-08-10"),
                ("2024-08-11", "2024-08-15"),
                ("2024-08-16", "2024-08-20"),
            ],
            3,
        ),
    ],
)
async def test_add_and_get_my_bookings(
    dates,
    expected_count,
    authenticated_ac,
    test_room,
):
    # добавляем бронирования
    for date_from, date_to in dates:
        response = await authenticated_ac.post(
            "/bookings/",
            json={
                "room_id": test_room.id,
                "hotel_id": test_room.hotel_id,
                "date_from": date_from,
                "date_to": date_to,
            },
        )
        assert response.status_code == 200

    # получаем свои бронирования
    response = await authenticated_ac.get("/bookings/me")
    assert response.status_code == 200

    data = response.json()

    if isinstance(data, dict) and "data" in data:
        bookings = data["data"]
    else:
        bookings = data

    assert len(bookings) == expected_count