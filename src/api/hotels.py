from datetime import date
from fastapi import HTTPException, Query, Body, APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy import func, insert, select


from exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, ObjectNotFoundException
from src.services.hotels import HotelService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

# ТУТ Я ПРОПИСАЛА prefix = "/hotels" и ко всем ручкам у которых есть этот роутер, не надо прописывать префиксыы вот так # @router.get("/hotels")
# ВЕДЬ МЫ УЖЕ ПРОПИСАЛИ ПРЕФИКС В РОУТЕР

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels = await HotelService(db).get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        pagination=pagination,
    )
    return {"status": "ok", "data": hotels}


@router.get("/{hotel_id}")
async def edit_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400,detail="Отель не найден")



@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException()

# body, requetst body
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звёзд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Дубай шикарный отель", "location": "ул. Шейха, 2"},
            },
        }
    ),
):
    # hotel_data.model_dump() возвращает словарь типа:
    # {'name': 'Hilton', 'location': 'Москва', 'rooms_quantity': 100, ...}

    # Две звездочки ** "распаковывают" словарь в именованные аргументы
    # execute в переводе - исполни
    # compile() значит скомпилируй  логирование
    # print(add_hotel_stmt.compile(engine,compile_kwargs={"literal_binds":True}))
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "ok", "data": hotel}


# @app.get("/")
# def func():
#     return "Hello WORLD!"

# put отправить все параметры сущности кроме айдшника. меняем только title name если не всё передастся  то ошибка
# patch там можно передать либо title лбио name (либо и то и то, но это уже put) puch создан чтоб редачиь один пареметр по сути


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновлением данные об оетле. можно отправить name, а можно title",
)
async def partilly_edit_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).partilly_edit_hotel(hotel_id=hotel_id, hotel_data=hotel_data)
    return {"status": "ok"}

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    # КОММИТ НА УРОВНЕ РУЧКИ ПРОИСХОДИТ!!!!!!!!!!
    return {"status": "ok"}