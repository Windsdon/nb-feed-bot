import asyncio

from bot.config import config
from bot.discord import post_message
from bot.feed import read_feed
from bot.opengraph import fetch_post_details


def main():
    entries = read_feed(config.feed_url)

    for entry in entries:
        details = fetch_post_details(entry.link)

        post_message(config.webhook_url, details)
        asyncio.sleep(1)


if __name__ == '__main__':
    main()
