from src.models.users import UserOrm
from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.bookings import BookingRead
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(RoomDataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = BookingRead


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
