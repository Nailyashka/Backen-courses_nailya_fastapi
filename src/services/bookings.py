from fastapi import HTTPException

from exceptions import AllRoomsAreBookedExcepion, ObjectNotFoundException, RoomNotFoundHTTPException
from schemas.bookings import BookingAdd, BookingAddRequest
from src.services.base import BaseService


class BookingService(BaseService):
    
    async def get_bookings_by_user(self, user_id: int):
        return await self.db.bookings.get_by_user(user_id=user_id)
    
    async def add_booking(
                        self,
                        user_id: int,
                        booking_data: BookingAddRequest):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException()
        
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(
                _booking_data,
                hotel_id=booking_data.hotel_id,
            )
        except AllRoomsAreBookedExcepion:
            raise AllRoomsAreBookedExcepion()
        except Exception:
            raise NameError(status_code=500, type="InternalError", detail="Ошибка сервера")
        
        await self.db.commit()
        return booking