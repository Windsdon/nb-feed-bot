from logging import Logger
from urllib.error import URLError

from celery import Celery
from celery.utils.log import get_task_logger

from bot.config import config, load_sources
from bot.discord import post_message
from bot.feed import read_feed
from bot.models import FeedEntry, PostDetails, FeedConfig
from bot.opengraph import fetch_post_details
from bot.storage import get_published_list

app = Celery('tasks', broker=config.broker)

logger: Logger = get_task_logger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, check_sources_task.s(), name='check sources every 60 seconds')
    check_sources_task.delay()


@app.task
def check_sources_task():
    sources = load_sources()

    for feed_id, feed in sources.items():
        check_posts_task.delay(feed_id, feed.dict())


@app.task
def check_posts_task(feed_id: str, feed: dict):
    feed = FeedConfig.parse_obj(feed)

    published_list = get_published_list(feed_id)
    entries = read_feed(feed.feed_url)
    logger.info(f'Got {len(entries)} entries for feed {feed_id}')

    if len(published_list) == 0:
        logger.info('Will not post anything because this is the first run')

        # fill with all entry ids
        for entry in entries:
            published_list.append(entry.id)

        return

    for entry in entries:
        if entry.id not in published_list:
            logger.info(f'Entry published at {entry.published} will be posted')
            prepare_entry_task.delay(entry.dict(), feed.dict())
            published_list.append(entry.id)


@app.task(autoretry_for=(URLError, OSError), retry_backoff=True)
def prepare_entry_task(entry: dict, feed: dict):
    entry = FeedEntry.parse_obj(entry)
    feed = FeedConfig.parse_obj(feed)

    details = fetch_post_details(entry.link, feed)
    send_message_task.delay(details.dict())


@app.task(rate_limit='1/s')
def send_message_task(details: dict):
    details = PostDetails.parse_obj(details)
    post_message(details)
