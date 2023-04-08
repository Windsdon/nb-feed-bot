import time

from bot.config import load_sources
from bot.discord import post_message
from bot.feed import read_feed
from bot.opengraph import fetch_post_details
from bot.storage import get_published_list


def main():
    sources = load_sources()

    for feed_id, feed in sources.items():
        entries = read_feed(feed.feed_url)
        published_list = get_published_list(feed_id)

        if len(published_list) == 0:
            # this is the first run, append everything and skip posting
            for entry in entries:
                published_list.append(entry.id)

            continue

        for entry in entries:
            if entry.id in published_list:
                continue

            details = fetch_post_details(entry.link, feed)

            post_message(details)
            published_list.append(entry.id)
            time.sleep(1)


if __name__ == '__main__':
    main()
