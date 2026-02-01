from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    # schema: BaseModel = None
    mapper: DataMapper = None
    # будет принимать сессию из вне чтоб постоянно не открывать её. ату вдруг подряд будет вызвано две функции 
    # и если будет открываться сессия то получается уже два соединения будет
    #  а елси прокинуть так,то будет только одно соединение к базе данных
    def __init__(self, session):
        self.session = session
        
    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        # *НЕ ПРИВЯЗЫВАЕМСЯ К СХЕМАМ
        #* return [self.schema.model_validate(model,from_attributes=True) for model in result.scalars().all()]
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
    
    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()
        
        
    async def get_one_or_none(self,**filter_by):
        # query - это select. остальное это stmt 
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            model = result.scalars().one_or_none()
            if model is None:
                return None
            return self.mapper.map_to_domain_entity(model)
                
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
    
    # bulk = много данных.массивный
    async def add_bulk(self, data:list[ BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)
    
    async def edit(self, data: BaseModel,exclude_unsert: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unsert))
            )
        
        await self.session.execute(update_stmt)
        
        
    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
    