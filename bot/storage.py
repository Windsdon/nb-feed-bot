from redis import Redis

from bot.config import config


# from https://gist.github.com/mjallday/3988344
class RedisCircularBuffer:
    def __init__(self, namespace: str, size: int, redis: Redis):
        self.namespace = namespace
        self.size = size
        self.redis = redis

    def append(self, item: str):
        self.redis.lpush(self.namespace, item)
        self.redis.ltrim(self.namespace, 0, self.size)

    def __iter__(self):
        return (x.decode('utf-8') if x is not None else None for x in self.redis.lrange(self.namespace, 0, self.size))

    def __len__(self):
        return self.redis.llen(self.namespace)

    def __contains__(self, item):
        return item in list(self)

    def __repr__(self):
        return '[' + ','.join(
            repr(x) for x in self
        ) + ']'


def get_redis():
    return Redis(host=config.redis_host, port=int(config.redis_port), db=int(config.redis_db_app))


def get_published_list(feed_id: str, buffer_len: int = 100):
    return RedisCircularBuffer(feed_id, buffer_len, get_redis())
