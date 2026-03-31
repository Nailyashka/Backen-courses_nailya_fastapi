from fastapi import Query, Body, APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import func, insert, select


from src.services.facility import FacilityService
from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep, PaginationDep


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Взять все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("", summary="Добавить удобства")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilityService(db).create_facility(facility_data)

    return {"status": "OK", "data": facility}
