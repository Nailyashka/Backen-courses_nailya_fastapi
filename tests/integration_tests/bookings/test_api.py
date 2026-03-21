from datetime import datetime
import pytest_asyncio
import pytest
from src.utils.db_manager import DBManager
from tests.conftest import db  

async def print_bookings(db):
    all_bookings = await db.bookings.get_all()
    print("\n--- Current bookings in DB ---")
    if not all_bookings:
        print("Нет бронирований в базе")
    for b in all_bookings:
        print(f"Room {b.room_id}, Hotel {b.hotel_id}, {b.date_from} -> {b.date_to}")
    print("-----------------------------\n")
# -----------------------------
# Очистка бронирований перед каждым тестом
# -----------------------------
@pytest_asyncio.fixture(autouse=True)
async def clean_bookings(db):
    """Удаляем все бронирования перед каждым тестом"""
    await db.bookings.delete()
    await db.commit()
    yield

# -----------------------------
# Тест добавления бронирования
# -----------------------------
@pytest.mark.parametrize(
    "room_id, date_from, date_to, expected_status",
    [
        (1, "2024-08-01", "2024-08-10", 200),
        (1, "2024-08-02", "2024-08-11", 200),
        (1, "2024-08-03", "2024-08-12", 200),
        (1, "2024-08-04", "2024-08-13", 200),
        (1, "2024-08-05", "2024-08-14", 200),
        # (1, "2024-08-06", "2024-08-15", 500),  # конфликт бронирования
        (1, "2024-08-17", "2024-08-25", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, expected_status, authenticated_ac, db):
    await print_bookings(db)
    rooms = await db.rooms.get_all()
    print("Rooms in DB:", rooms)
    if not rooms:
        pytest.fail("Нет комнат в базе для теста!")
    room = rooms[0]
    r_id, h_id = room.id, room.hotel_id

    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": r_id,
            "hotel_id": h_id,
            "date_from": date_from,  # строка "2024-08-01"
            "date_to": date_to,      # строка "2024-08-10"
        }
)
    print("\n--- RESPONSE DEBUG ---")
    print("Status code:", response.status_code)
    try:
        print("JSON:", response.json())
    except Exception as e:
        print("Не удалось распарсить JSON:", e)
    print("Headers:", response.headers)
    print("----------------------\n")

    if response.status_code != expected_status:
        print("\n--- DEBUG INFO ---")
        print("Response JSON:", response.json())
        print("Expected status:", expected_status)
        print("Actual status:", response.status_code)
        print("------------------")

    assert response.status_code == expected_status
    if response.status_code == 200:
        res = response.json()
        assert res["status"] == "ok"

# -----------------------------
# Тест получения своих бронирований
# -----------------------------
@pytest.mark.parametrize(
    "room_id, date_from, date_to, expected_count",
    [
        (1, "2024-08-01", "2024-08-10", 1),
        (1, "2024-08-02", "2024-08-11", 2),
        (1, "2024-08-03", "2024-08-12", 3),
    ],
)
async def test_add_and_get_my_bookings(room_id, date_from, date_to, expected_count, authenticated_ac, db):
    rooms = await db.rooms.get_all()
    print("Rooms in DB:", rooms)
    if not rooms:
        pytest.fail("Нет комнат в базе для теста!")
    room = rooms[0]
    r_id, h_id = room.id, room.hotel_id

    response = await authenticated_ac.post(
        "/bookings/",
        json={
            "room_id": r_id,
            "hotel_id": h_id,
            "date_from": date_from,  # строка "2024-08-01"
            "date_to": date_to,      # строка "2024-08-10"
        }
    )
    assert response.status_code == 200

    # Получаем свои бронирования
    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert response_my_bookings.status_code == 200

    res_data = response_my_bookings.json()
    actual_count = len(res_data["data"]) if isinstance(res_data, dict) and "data" in res_data else len(res_data)
    assert actual_count == expected_count