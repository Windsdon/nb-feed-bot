from typing import Optional

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
    published: str


class FeedConfig(BaseModel):
    webhook_url: str
    feed_url: str
    colour: str
    name: Optional[str]
    avatar: Optional[str]


class PostDetails(BaseModel):
    url: str
    title: str
    description: str
    image_url: str
    feed: FeedConfig


class FeedConfigFile(BaseModel):
    feeds: dict[str, FeedConfig]


if __name__ == '__main__':
    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.realpath(os.path.join(dir_path, '../__schemas__/FeedConfigFile.json')), 'wt') as f:
        f.write(FeedConfigFile.schema_json(indent='\t'))
