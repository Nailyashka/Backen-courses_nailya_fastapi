from fastapi import HTTPException, Query, Body, APIRouter, Depends
from sqlalchemy import func, insert, select


from exceptions import AllRoomsAreBookedExcepion, ObjectNotFoundExcepion
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, PaginationDep, UserIdDepends
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDepends, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(user_id: UserIdDepends, db: DBDep, booking_data: BookingAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundExcepion:
        raise HTTPException(status_code=400, detail="Номер не найден")
    # if not room:
    #     raise HTTPException(status_code=404,detail="Номер не найден")
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=booking_data.hotel_id)
    except AllRoomsAreBookedExcepion:
        raise HTTPException(status_code=409,detail="Не осталось свободных номеров")
    await db.commit()
    # Полуцчить цену номера
    # Создать схему данных BookingAdd
    # Добавить бронирование конкретному пользователю
    return {"status": "ok", "data": booking}
