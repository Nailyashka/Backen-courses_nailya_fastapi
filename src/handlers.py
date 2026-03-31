from fastapi.responses import JSONResponse
from fastapi import Request

from src.exceptions import AllRoomsAreBookedExcepion, HotelNotFoundHTTPException, RoomNotFoundHTTPException


async def booking_exception_handler(request: Request, exc: AllRoomsAreBookedExcepion):
    return JSONResponse(
        status_code=409,
        content={"detail": "Не осталось свободных номеров"}
    )
    
async def hotel_not_found_handler(request, exc: HotelNotFoundHTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Отель не найден"}
    )


async def room_not_found_handler(request, exc: RoomNotFoundHTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Комната не найдена"}
    )