from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, check_date_to_after_date_from
from src.schemas.hotels import HotelAdd
from src.services.base import BaseService



class HotelService(BaseService):
    async def get_filtered_by_time(self,
                                    date_from: str,
                                    date_to: str,
                                    location: str | None = None,
                                    title: str | None = None,
                                    pagination: dict | None = None,
                                    ):
        check_date_to_after_date_from(date_from,date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        
    async def get_hotel(self,hotel_id: int):
        try:
            return await self.db.hotels.get_one(id=hotel_id) 
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException()   
        
    async def add_hotel(self, hotel_data: HotelAdd):    
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel
    
    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
        
    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()
        
    async def partilly_edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, exclude_unsert=True, id=hotel_id)
        await self.db.commit()