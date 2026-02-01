from fastapi import Query, Body,APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import func, insert, select


from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep, PaginationDep


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Взять все удобства")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()


@router.post("", summary="Добавить удобства")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}