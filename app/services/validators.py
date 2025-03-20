from redis import Redis

from core.exeptions import (MissingToken, TokenBlacklisted,
                            TokenNotInWhitelist, UserNotFound)
from schemas.token import TokenList
from schemas.user import User

USER_NOT_FOUND = 'Пользователь с данным токеном не найден'
TOKEN_BLACKLISTED = 'Токен отозван'
UNKNOWN_TOKEN = 'Неизвестный токен'
MISSING_TOKEN = 'В заголовке http запроса отсутствует Bearer токен'


async def is_user(user: User | None) -> None:
    '''Существует ли пользователь'''
    if not user:
        raise UserNotFound(USER_NOT_FOUND)


async def is_token(token: str | None) -> None:
    '''Существует ли токен'''
    if not token:
        raise MissingToken(MISSING_TOKEN)


async def is_token_blacklisted(token: str, redis: Redis) -> None:
    '''Находится ли токен в Blacklist'''
    tokens = redis.get(token)
    if tokens and tokens.decode("utf-8") == TokenList.BLACKLIST:
        raise TokenBlacklisted(TOKEN_BLACKLISTED)


async def is_token_whitelisted(token: str, redis: Redis) -> None:
    '''Находится ли токен в Whitelist'''
    tokens = redis.get(token)
    if not tokens or tokens.decode("utf-8") != TokenList.WHITELIST:
        raise TokenNotInWhitelist(UNKNOWN_TOKEN)
