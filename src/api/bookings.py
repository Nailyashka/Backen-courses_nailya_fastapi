from fastapi import HTTPException, Query, Body, APIRouter, Depends
from sqlalchemy import func, insert, select


from src.exceptions import AllRoomsAreBookedExcepion, ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, PaginationDep, UserIdDepends
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH
print("BOOKINGS ROUTER LOADED")

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

for r in router.routes:
    print(r.path, r.methods)

@router.get("/")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDepends, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("/")
async def add_booking(user_id: UserIdDepends, db: DBDep, booking_data: BookingAddRequest):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException()

    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )

    try:
        booking = await db.bookings.add_booking(_booking_data)
    except AllRoomsAreBookedExcepion:
        raise HTTPException(status_code=409, detail="Не осталось свободных номеров")
    except Exception as e:
        print("Ошибка бронирования:", e)
        raise HTTPException(status_code=500, detail=str(e))

    await db.commit()

    return {"status": "ok", "data": booking}