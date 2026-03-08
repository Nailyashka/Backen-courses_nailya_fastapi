from datetime import date

from fastapi import HTTPException


class  NabronirovalExcepion(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self,*args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalExcepion):
    detail = "Объект не найден"
    
class ObjectAlreadyExistsExcepion(NabronirovalExcepion):
    detail = "Похожий объект уж существует"
    
class AllRoomsAreBookedExcepion(NabronirovalExcepion):
    detail = "Не осталось свободных номеров"
    
class UserAlreadyExists(NabronirovalExcepion):
    detail = "Пользователь с таким email уже сущствует"
    
def check_date_to_after_date_from(date_from:date,date_to:date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code = 422, detail="Дата заезда не может быть позже даты выезда")
    
    
class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"