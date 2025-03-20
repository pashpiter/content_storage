import bcrypt
from sqlmodel import Session

from core.exeptions import (ForbiddenAddContent, IncorrectPassword,
                            UserAlreadyExsist, UserNotFound)
from db.crud import select_user_by_email
from schemas.user import User, UserRoles

USER_ALREADY_EXSIST = 'Пользователь с email={} уже существует.'
INCORRECT_PASSWORD = 'Неверный пароль.'
FORRBIDDEN_FOR_CLIENT = 'Доступ запрещен.'
USERS_NOT_FOUND = 'Ниодного пользователя не найдено'
USER_NOT_FOUND = 'Пользователь не найден'


async def check_user_exsists(email: str, session: Session) -> None:
    '''Проверка что пользователь с таким email уже существует'''
    user = await select_user_by_email(email, session)
    if user:
        raise UserAlreadyExsist(USER_ALREADY_EXSIST.format(email))


async def check_password(text_password: str, hashed_password: str) -> None:
    '''Проверка пароля пользователя'''
    if not bcrypt.checkpw(text_password, hashed_password):
        raise IncorrectPassword(INCORRECT_PASSWORD)


async def is_admin(user: User) -> None:
    '''Првоерка что прользователь админ'''
    if not user.role == UserRoles.ADMIN:
        raise ForbiddenAddContent(FORRBIDDEN_FOR_CLIENT)


async def is_one_user(users: list[User] | None) -> None:
    '''Проверка что есть хоть один пользователь'''
    if not users:
        raise UserNotFound(USERS_NOT_FOUND)


async def is_user_in_db(user: User | None) -> None:
    '''Проверка что есть пользователь'''
    if not user:
        raise UserNotFound(USER_NOT_FOUND)
