from datetime import date
from sqlalchemy import func, select
from src.repositories.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_bookings

from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    # get_all параметры именую уже как ближе к бд отностяся строки

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotel]:

        rooms_ids_to_get = rooms_ids_for_bookings(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%")
            )
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)

        # await - это мы к базе идём. остлаьные дейтсвия ниже это работа  с итератором
        # return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
