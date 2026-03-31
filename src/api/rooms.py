from datetime import date
from fastapi import HTTPException, Query, Body, APIRouter, Depends

from exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundHTTPException, check_date_to_after_date_from
from src.services.rooms import RoomService
from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    await RoomService(db).get_filtered_by_time(date_from=date_from, date_to=date_to,hotel_id = hotel_id)
    return {"status": "ok"}
    


# @router.get("/{hotel_id}/rooms/{room_id}")
# async def edit_room(hotel_id: int, room_id: int, db: DBDep):
#         return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id = hotel_id)


@router.post("/{hotel_id}/rooms", summary="Добавить комнату")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()
    return {"status": "ok", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
        return {"status": "ok"}



@router.patch(
    "/{hotel_id}/rooms/{room_id}",
)
async def partilly_edit_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    return await RoomService(db).partially_edit_room(
            hotel_id=hotel_id,
            room_id=room_id,
            room_data=room_data
        )
    
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "ok"}
