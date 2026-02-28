
class  NabronirovalExcepion(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self,*args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundExcepion(NabronirovalExcepion):
    detail = "Объект не найден"
    
class AllRoomsAreBookedExcepion(NabronirovalExcepion):
    detail = "Не осталось свободных номеров"
    