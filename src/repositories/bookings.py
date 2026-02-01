from datetime import date
from sqlalchemy import func, select


from src.repositories.mappers.mappers import BookingDataMapper
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking
from src.repositories.base import BaseRepository


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
    
    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all() ]