import requests
from discord import SyncWebhook, Embed, Colour
from discord.utils import MISSING

from bot.models import PostDetails


def post_message(details: PostDetails):
    with requests.Session() as session:
        webhook = SyncWebhook.from_url(details.feed.webhook_url, session=session)
        embed = Embed(
            colour=Colour.from_str(details.feed.colour),
            title=details.title,
            type='rich',
            url=details.url,
            description=details.description,
        ).set_image(url=details.image_url)

        webhook.send(
            embed=embed,
            username=details.feed.name or MISSING,
            avatar_url=details.feed.avatar or MISSING
        )
