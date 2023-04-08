from opengraph_py3 import OpenGraph

from bot.models import PostDetails, FeedConfig


def fetch_post_details(url: str, feed: FeedConfig):
    og = OpenGraph(url=url)
    return PostDetails(
        url=url,
        title=og.get('title'),
        description=og.get('description'),
        image_url=og.get('image'),
        feed=feed
    )
