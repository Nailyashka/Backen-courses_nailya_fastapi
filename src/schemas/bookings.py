from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date
    
class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int
    
class BookingRead(BookingAdd):
    id: int
    
class Booking(BookingAdd):
    user_id: int

    