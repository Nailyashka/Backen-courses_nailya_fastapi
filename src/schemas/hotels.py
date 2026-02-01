from pydantic import BaseModel,ConfigDict

class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int
    # тут можно убрать (from_attributes=True) так как есть datamapper
    
class HotelPATCH(BaseModel):
    #Совет вместо Field(None) можно использовать просто None
    #А также нужно обязательно указывать значение по умолчанию Field(None)
    title: str | None = None
    location: str | None= None