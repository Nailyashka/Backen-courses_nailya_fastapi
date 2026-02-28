from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: EmailStr
    hashed_passworld: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_passworld: str
