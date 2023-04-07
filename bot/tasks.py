import time
from logging import Logger

from celery import Celery
from celery.utils.log import get_task_logger

from bot.config import config
from bot.discord import post_message
from bot.feed import read_feed
from bot.models import FeedEntry
from bot.opengraph import fetch_post_details
from bot.storage import get_last_published_timestamp, set_last_published_timestamp

app = Celery('tasks', broker=config.broker)

logger: Logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, check_posts_task.s(), name='check posts every 60 seconds')
    check_posts_task.delay()


@app.task
def check_posts_task():
    last_published_ts = get_last_published_timestamp()
    logger.info(f'Last published: {last_published_ts}')
    entries = read_feed(config.feed_url)
    logger.info(f'Got {len(entries)} entries')

    new_last_published = sorted([e.published for e in entries])[-1]
    set_last_published_timestamp(new_last_published)
    logger.info(f'Last published updated to: {new_last_published}')

    for entry in entries:
        logger.info(f'Processing entry published at {entry.published}')
        if last_published_ts is None or entry.published > last_published_ts:
            post_message_task.delay(entry.dict())


@app.task(rate_limit='1/s')
def post_message_task(entry: dict):
    entry = FeedEntry.parse_obj(entry)
    # logger.info(f'Fetching details for {entry.dict()}')
    details = fetch_post_details(entry.link)
    # logger.info(f'Would post: {details.dict()}')
    post_message(config.webhook_url, details)