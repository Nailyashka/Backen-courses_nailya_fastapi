from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int


class RoomsFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacility(RoomsFacilityAdd):
    room_id: int
