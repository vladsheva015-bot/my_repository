from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, UserNotFoundException, \
    UserNotFoundHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["авторизация и аутентификация"])


@router.post("/register", summary="регистрация пользователя")
async def register_user(
        db: DBDep,
        data: UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}