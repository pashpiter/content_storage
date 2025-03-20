import redis

from core.config import settings


def redis_client() -> redis.Redis:
    return redis.Redis.from_url(settings.redis.redis_url)
