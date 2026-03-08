from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from sqlalchemy import select


from src.exceptions import UserAlreadyExists
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword
from src.models.users import UserOrm
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)
    
    async def add(self, data: BaseModel):
        try:
            return await super().add(data)
        except IntegrityError:
            raise UserAlreadyExists()
