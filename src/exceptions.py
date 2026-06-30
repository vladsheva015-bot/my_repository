from datetime import date

from fastapi import HTTPException


class CLSException(Exception):
    detail ="Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(CLSException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(CLSException):
    detail = "Похожий Объект же существует"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class AllRoomsAreBookedException(CLSException):
    detail = "Не осталось свободных номеров"

class IncorrectTokenException(CLSException):
    deatil = "Некорректный токен"


def check_date_to_after_date_from(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата выезда не может быть позже даты заезда")



class CLSHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(CLSHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(CLSHTTPException):
    status_code = 404
    detail = "Номер не найден"

class IncorrectTokenHTTPException(CLSHTTPException):
    detail = "Некорректный токен"

class UserAlreadyExistsException(CLSException):
    detail = "Пользователь уже существует"

class UserNotFoundException(CLSException):
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordException(CLSException):
    detail = "Пароль неверный"

class AllRoomsAreBookedHTTPException(CLSHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"

class UserEmailAlreadyExistsHTTPException(CLSHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class UserNotFoundHTTPException(CLSHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordHTTPException(CLSHTTPException):
    status_code = 401
    detail = "Пароль неверный"