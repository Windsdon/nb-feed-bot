import time

from pydantic import BaseModel


class FieldContent(BaseModel):
    type: str
    value: str


class FieldMedia(BaseModel):
    width: int
    height: int
    url: str


class FeedEntry(BaseModel):
    id: str
    link: str
    title: str
    content: list[FieldContent]
    media_thumbnail: list[FieldMedia]
    published: str


class PostDetails(BaseModel):
    url: str
    title: str
    description: str
    image_url: str
    colour: str
