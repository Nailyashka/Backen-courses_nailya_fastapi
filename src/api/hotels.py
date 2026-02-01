from datetime import date
from fastapi import Query, Body,APIRouter, Depends
from sqlalchemy import func, insert, select


from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

#ТУТ Я ПРОПИСАЛА prefix = "/hotels" и ко всем ручкам у которых есть этот роутер, не надо прописывать префиксыы вот так # @router.get("/hotels")
#ВЕДЬ МЫ УЖЕ ПРОПИСАЛИ ПРЕФИКС В РОУТЕР

router = APIRouter(prefix="/hotels" , tags=["Отели"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
    location: str | None = Query(None,description="Локация"),
    title: str | None= Query(None,description='Название отеля'),
):
    
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page-1))
    
        
@router.get("/{hotel_id}")
async def edit_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)
    
          
@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    # КОММИТ НА УРОВНЕ РУЧКИ ПРОИСХОДИТ!!!!!!!!!!
    return {"status":"ok"}

#body, requetst body
@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(openapi_examples={
        "1":{"summary":"Сочи", "value":{
            "title":"Отель Сочи 5 звёзд у моря",
            "location":"ул. Моря, 1"
        }},
        "2":{"summary":"Дубай", "value":{
            "title":"Дубай шикарный отель",
            "location":"ул. Шейха, 2"
        }}
    }),
    
):
    # hotel_data.model_dump() возвращает словарь типа:
# {'name': 'Hilton', 'location': 'Москва', 'rooms_quantity': 100, ...}

# Две звездочки ** "распаковывают" словарь в именованные аргументы
    hotel = await db.hotels.add(hotel_data)
        # execute в переводе - исполни
        # compile() значит скомпилируй  логирование
        # print(add_hotel_stmt.compile(engine,compile_kwargs={"literal_binds":True}))
    return {"status":"ok"}

# @app.get("/")
# def func():
#     return "Hello WORLD!"

#put отправить все параметры сущности кроме айдшника. меняем только title name если не всё передастаться  то ошибка
#patch там можно передать либо title лбио name (либо и то и то, но это уже put) puch создан чтоб редачиь один пареметр по сути 

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int,hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    return {"status":"ok"}    
        
@router.patch(
    "/{hotel_id}", 
    summary='Частичное обновление данных об отеле',
    description="Тут мы частично обновлением данные об оетле. можно отправить name, а можно title")


async def partilly_edit_hotel(hotel_id: int,
                hotel_data: HotelPATCH, db: DBDep
               ):
    await db.hotels.edit(hotel_data,exclude_unsert=True,id=hotel_id)