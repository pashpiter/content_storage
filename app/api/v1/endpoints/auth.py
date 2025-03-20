from datetime import datetime

from fastapi import APIRouter, Depends, Header
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.validators import check_password, check_user_exsists, is_user_in_db
from core.config import settings
from core.redis import redis_client
from db.crud import create_user, select_user_by_email
from db.database import get_session
from schemas.token import TokenList, TokenRead
from schemas.user import User, UserCreate, UserRead
from services.token import create_token, decode_verify_token
from services.user import create_hashed_password, get_user

SECONDS_IN_MINUTE = 60

router = APIRouter(prefix='/auth')


@router.post('/login')
async def login(
        user_create: UserCreate,
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(redis_client)
) -> TokenRead:
    '''Получение токена и добавление токена в whitelist'''
    user = await select_user_by_email(user_create.email, session)
    await is_user_in_db(user)
    await check_password(user_create.password, user.hash_password)
    token = await create_token(user_create)
    redis.setex(
        token,
        settings.app.access_token_expire_minutes*SECONDS_IN_MINUTE,
        TokenList.WHITELIST
    )
    return TokenRead(access_token=token)


@router.post('/signup')
async def signup(
        user_create: UserCreate,
        session: AsyncSession = Depends(get_session)
) -> UserRead:
    '''Регистрация пользователя'''
    await check_user_exsists(user_create.email, session)
    user_dump = user_create.model_dump()
    user_dump['hash_password'] = await create_hashed_password(
        user_create.password
    )
    new_user = await create_user(user_dump, session)
    return new_user


@router.post('/logout')
async def logout(
        user: User = Depends(get_user),
        token: str | None = Header(default=None, alias='Authorization'),
        redis: Redis = Depends(redis_client)
) -> dict:
    '''Выход пользователя и добавление токена в blacklist'''
    token = token.split()[-1]
    payload = await decode_verify_token(token)
    exp_time: int = payload['exp']
    remain_time = exp_time - int(datetime.now().timestamp())
    redis.setex(token, remain_time, TokenList.BLACKLIST)
    return {'message': 'Вы вышли из системы.'}
