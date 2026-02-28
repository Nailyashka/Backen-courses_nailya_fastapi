from src.database import Base

from typing import TypeVar
from pydantic import BaseModel

DBModelType = TypeVar("DBModelType", bound=Base)
ShemaType = TypeVar("ShemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[ShemaType] = None

    @classmethod
    # Превращаем sql- модель в pydantic схему
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persinstance_entity(cls, data):
        return cls.db_model(**data.model_dump())
