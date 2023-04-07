from opengraph_py3 import OpenGraph

from bot.config import config
from bot.models import PostDetails


def fetch_post_details(url: str):
    og = OpenGraph(url=url)
    return PostDetails(
        url=url,
        title=og.get('title'),
        description=og.get('description'),
        image_url=og.get('image'),
        colour=config.colour
    )
