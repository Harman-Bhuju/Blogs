from sqlalchemy.orm import configure_mappers

from blogs.common.models import BaseModel
from blogs.features.comments.models import Comment
from blogs.features.posts.models import Post
from blogs.features.tags.models import PostTag, Tag
from blogs.features.users.models import User


def register_models() -> None:
    """Ensure all SQLAlchemy models are registered and their relationships configured.

    Why this is needed:
    1. Import Registration:
       The imports above (Comment, Post, Tag, PostTag, User) execute the class
       definitions so that SQLAlchemy's DeclarativeBase becomes aware of all tables.

    2. configure_mappers():
       SQLAlchemy relationships use 'Two-Phase Mapping'. When model classes are first
       loaded, relationships defined with string targets (e.g. Mapped['User']) are
       stored as pending references.
       
       Calling configure_mappers():
       - Traverses all registered models.
       - Resolves all string references to their actual Python classes.
       - Verifies foreign keys and matches two-way back_populates declarations.
       - Wires relationship properties in memory before any database query runs.
       
       By calling this explicitly at application startup (in main.py) and in Alembic
       (in env.py), any missing model imports, typos, or relationship misconfigurations
       will fail fast immediately on launch with a clear error stack, rather than
       failing lazily during a live user request in production.
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
