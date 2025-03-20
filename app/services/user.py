import bcrypt

from fastapi import Depends, Header
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.redis import redis_client
from db.crud import select_user_by_email
from db.database import get_session
from schemas.user import User
from services.token import decode_verify_token
from services.validators import (is_token, is_token_blacklisted,
                                 is_token_whitelisted, is_user)


async def create_hashed_password(text_password: str) -> str:
    '''Создание зашифрованного пароля'''
    return bcrypt.hashpw(text_password, bcrypt.gensalt())


async def get_user(
    token: str | None = Header(default=None, alias='Authorization'),
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(redis_client)
) -> User:
    '''Проверка валидности токена и поулчение пользователя из запроса'''
    await is_token(token)
    token = token.split()[-1]
    await is_token_blacklisted(token, redis)
    await is_token_whitelisted(token, redis)
    payload = await decode_verify_token(token.split()[-1])
    user = await select_user_by_email(payload['email'], session)
    await is_user(user)
    return user
