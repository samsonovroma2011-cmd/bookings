from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep

from src.exeptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException, IncorrectPasswordException, \
    IncorrectPasswordHTTPException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, UserNotFoundException, \
    UserNotFoundHTTPException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router.post("/register")
async def register_user(
        data: UserRequestAdd,
        db: DBDep
):
    try:
        user = await AuthService(db).register_user(data=data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException

    return {"status_code": 200, "data": user}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep
):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/me")
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):
    try:
        user = await AuthService(db).get_me(user_id=user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException

    return user

@router.post("/logout")
async def logout(response: Response):

    response.delete_cookie("access_token")
    return {"status_code": 200}