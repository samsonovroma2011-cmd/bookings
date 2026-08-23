from datetime import date

from fastapi import HTTPException


class BaseObjectException(Exception):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseObjectException):
    status_code = 404
    detail = "Объект не найден"


class AllRoomsAreBookedException(BaseObjectException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistsException(BaseObjectException):
    status_code = 409
    detail = "Объект уже существует"


class HotelNotExistException(BaseObjectException):
    status_code = 404
    detail = "Отель не существует"


class RoomNotExistException(BaseObjectException):
    status_code = 404
    detail = "Номер не существует"

class HotelNotFoundException(BaseObjectException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundException(BaseObjectException):
    status_code = 404
    detail = "Номер не найден"

class UserAlreadyExistsException(BaseObjectException):
    status_code = 409
    detail = "Пользователь уже существует"

class IncorrectPasswordException(BaseObjectException):
    status_code = 401
    detail = "Неверный пароль"

class IncorrectAccessTokenException(BaseObjectException):
    status_code = 401
    detail = "Неверный токен"

class EmailNotRegisteredException(BaseObjectException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"


def check_date_to_after_date_from(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден"

class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"

class UserAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Пользователь уже существует"

class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Неверный пароль"

class EmailNotRegisteredHTTPException(BaseObjectException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"