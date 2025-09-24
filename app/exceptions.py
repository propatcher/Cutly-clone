from fastapi import HTTPException,status

class DefaultException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(DefaultException):
    status_code=status.HTTP_409_CONFLICT
    detail="Пользователь уже существует"

class IncorrectEmailOrPasswordException(DefaultException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверная почта или пароль"

class TokenExpiredException(DefaultException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истёк"

class TokenAbsentException(DefaultException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"

class LinkAlreadyExistException(DefaultException):
    status_code=status.HTTP_409_CONFLICT
    detail="У вас уже есть эта ссылка"
    
class LinkNotExistException(DefaultException):
    status_code = status.HTTP_204_NO_CONTENT
    detail="Ссылки не существует"
class IncorrectTokenFormatException(DefaultException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неправильный формат токен"

class UserIsNotPresentException(DefaultException):
    status_code=status.HTTP_401_UNAUTHORIZED