from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundHTTPException, check_date_to_after_date_from
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch
from src.services.base import BaseService


class RoomService(BaseService):
    async def get_filtered_by_time(self,
                                   date_from: str,
                                   date_to: str,
                                   hotel_id: int):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        
    async def create_room(self,hotel_id: int, room_data:RoomAddRequest ):
        await self.db.hotels.get_one(id=hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        
        rooms_facilities_data = [
            RoomsFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]   
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room
    
    async def edit_room(self,
                        hotel_id:int,
                        room_id:int,
                        room_data: RoomAddRequest):
        try: 
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException() 
        
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException()
        
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()
        
    async def partilly_edit_room(self,
                                hotel_id: int,
                                room_id: int,
                                room_data: RoomAddRequest):
        
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException()
        
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException()
        
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id,
                facilities_ids=_room_data_dict["facilities_ids"]
            )

        await self.db.commit()

        return {"status": "ok"}
    
    async def get_room(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
        if not room:
            raise HotelNotFoundHTTPException()
        return room
        
    async def delete_room(self, hotel_id: int, room_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundHTTPException
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundHTTPException
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()
