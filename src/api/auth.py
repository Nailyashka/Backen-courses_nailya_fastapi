from fastapi import APIRouter, HTTPException, Response

from src.exceptions import ObjectAlreadyExistsExcepion, UserAlreadyExists
from src.api.dependencies import UserIdDepends
from src.services.auth import AuthService
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker

router = APIRouter(prefix="/auth", tags=["Авторизация и аутенфикация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_passworld = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_passworld=hashed_passworld)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        # execute в переводе - исполни
        # compile() значит скомпилируй  логирование
        # print(add_hotel_stmt.compile(engine,compile_kwargs={"literal_binds":True}))
            await session.commit()
        except ObjectAlreadyExistsExcepion:
            raise HTTPException(
                status_code=409,
                detail="пользоватль c таким email уже существует"
            )
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователя с таким email не зарегистрирован"
            )
        if not AuthService().verify_password(data.password, user.hashed_passworld):
            raise HTTPException(status_code=401, detail="Пароль неверный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    # execute в переводе - исполни
    # compile() значит скомпилируй  логирование
    # print(add_hotel_stmt.compile(engine,compile_kwargs={"literal_binds":True}))


@router.get("/me")
async def get_me(
    # FastAPI умный и записывает в request все параметры все query,cookie,headers...
    user_id: UserIdDepends,
):
    # а щас мы из cookie вытащили по сути jwt токен пользователя?
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/log_out")
async def log_out(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
