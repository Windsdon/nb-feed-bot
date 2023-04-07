from pydantic import BaseSettings


class BotConfig(BaseSettings):
    webhook_url: str
    feed_url: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db_celery: int = 0
    redis_db_app: int = 1
    colour = '#FF0000'

    @property
    def broker(self):
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db_celery}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = BotConfig()
