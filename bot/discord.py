import requests
from discord import SyncWebhook, Embed, Colour

from bot.models import PostDetails


def post_message(webhook_url: str, details: PostDetails):
    with requests.Session() as session:
        webhook = SyncWebhook.from_url(webhook_url, session=session)
        embed = Embed(
            colour=Colour.from_str(details.colour),
            title=details.title,
            type='rich',
            url=details.url,
            description=details.description,
        ).set_image(url=details.image_url)

        webhook.send(
            embed=embed
        )
