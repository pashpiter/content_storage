from http import HTTPStatus

from fastapi import HTTPException


class UserAlreadyExsist(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.CONFLICT, message)


class IncorrectPassword(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class ForbiddenAddContent(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class InvalidToken(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class ExpiredSignature(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class MissingToken(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class TokenBlacklisted(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class TokenNotInWhitelist(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class UserNotFound(HTTPException):
    def __init__(self, message: str):
        super().__init__(HTTPStatus.NOT_FOUND, message)
