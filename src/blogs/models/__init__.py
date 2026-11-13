from sqlalchemy.orm import configure_mappers

from blogs.common.models import BaseModel
from blogs.features.comments.models import Comment
from blogs.features.posts.models import Post
from blogs.features.tags.models import PostTag, Tag
from blogs.features.users.models import User


def register_models() -> None:
    """Load all database models and connect their relationships.

    How this works:
    1. Importing the models above (User, Post, Tag, PostTag, Comment) loads them into Python.
    2. configure_mappers() tells SQLAlchemy to connect all the relationships between them
       (for example, linking Post.author to User.posts).

    Why we do this at startup:
    If a model is missing or a relationship name has a typo, this will catch the error
    immediately when the app starts — instead of crashing later when a user makes a request!
    """
    configure_mappers()


__all__ = [
    "BaseModel",
    "Comment",
    "Post",
    "PostTag",
    "Tag",
    "User",
    "register_models",
]
