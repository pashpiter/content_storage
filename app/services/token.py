from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from core.config import settings
from core.exeptions import ExpiredSignature, InvalidToken
from schemas.user import UserCreate

EXPIRED_SIGNATIRE = 'Время использования токена вышло.'
INVALID_TOKEN = 'Невалидный токен.'


async def create_token(user: UserCreate) -> str:
    '''Создание токена'''
    data = user.model_dump(exclude='password')
    data['exp'] = datetime.now() + timedelta(
        minutes=settings.app.access_token_expire_minutes
    )
    token = jwt.encode(
        data,
        key=settings.app.secret_key,
        algorithm=settings.app.algorithm
    )
    return token


async def decode_verify_token(token: str) -> dict:
    '''Расшифровка токена'''
    try:
        payload = jwt.decode(
            token,
            key=settings.app.secret_key,
            algorithms=settings.app.algorithm
        )
    except ExpiredSignatureError:
        raise (ExpiredSignature(EXPIRED_SIGNATIRE))
    except InvalidSignatureError:
        raise (InvalidToken(INVALID_TOKEN))
    return payload
