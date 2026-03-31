from fastapi import HTTPException, Query, Body, APIRouter, Depends
from sqlalchemy import func, insert, select


from src.exceptions import AllRoomsAreBookedExcepion, ObjectNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest
from src.api.dependencies import DBDep, PaginationDep, UserIdDepends
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

for r in router.routes:
    print(r.path, r.methods)

# @router.get("/")
# async def get_bookings(
#     db: DBDep,
# ):
#     return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDepends, db: DBDep):
    await BookingService(db).get_bookings_by_user(user_id=user_id)
    return {"status": "ok"}

@router.post("/")
async def add_booking(
    user_id: UserIdDepends,
    db: DBDep,
    booking_data: BookingAddRequest
):
    booking = await BookingService(db).add_booking(
        user_id=user_id,
        booking_data=booking_data
    )

    return {"status": "ok", "data": booking}
  