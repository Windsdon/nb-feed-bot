from redis import Redis

from bot.config import config


def get_redis():
    return Redis(host=config.redis_host, port=int(config.redis_port), db=int(config.redis_db_app))


def get_last_published_timestamp() -> str | None:
    with get_redis() as db:
        value = db.get('last_timestamp')
        return value.decode('utf-8') if value else None


def set_last_published_timestamp(ts: str):
    with get_redis() as db:
        db.set('last_timestamp', ts)
