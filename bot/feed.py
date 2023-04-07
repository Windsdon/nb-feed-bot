import feedparser
from feedparser import FeedParserDict

from bot.models import FeedEntry


def read_feed(feed_url: str) -> list[FeedEntry]:
    feed = feedparser.parse(feed_url)
    entries: list[FeedParserDict] = feed['entries']

    return [FeedEntry.parse_obj(entry_raw) for entry_raw in entries]
