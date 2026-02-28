from datetime import date
from passlib.context import CryptContext
from schemas.users import UserAdd
from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("testpassword")

    user_data = UserAdd(email="test@example.com", hashed_passworld=hashed_password)

    user = await db.users.add(user_data)
    await db.commit()

    room_id = (await db.rooms.get_all())[0].id

    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )

    new_booking = await db.bookings.add(booking_data)

    # Получить эту бронь и убедиться, что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # а ещё модно вот так вот одни разом сравнить все парметры
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # ?обновить бронь

    updated_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user.id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=updated_date,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

    await db.commit()
