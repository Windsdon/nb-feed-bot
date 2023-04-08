import os
import re

import yaml
from pydantic import BaseSettings

from bot.models import FeedConfigFile, FeedConfig

_default_sources_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../sources'))

print(_default_sources_dir)

_valid_source_pattern = re.compile(r'^[^_]\w+\.yml$')


class BotConfig(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db_celery: int = 0
    redis_db_app: int = 1
    sources_dir: str = _default_sources_dir

    @property
    def broker(self):
        return f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db_celery}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = BotConfig()


def load_sources():
    sources: dict[str, FeedConfig] = {}

    for filename in os.listdir(config.sources_dir):
        if not _valid_source_pattern.match(filename):
            continue

        with open(os.path.join(config.sources_dir, filename), 'rt', encoding='utf-8') as f:
            source_dict = yaml.safe_load(f)
            config_file = FeedConfigFile.parse_obj(source_dict)

            for feed_id, feed in config_file.feeds.items():
                if feed_id in sources:
                    raise RuntimeError(f'Duplicated feed it: {feed}, currently checking file {filename}')

                sources[feed_id] = feed

    return sources
