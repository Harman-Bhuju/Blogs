from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import BaseModel

# Import related models only during static type checking.
# This helps type checkers understand relationship types
# without creating circular imports at runtime.
if TYPE_CHECKING:
    from blogs.comments.models.comment import Comment
    from blogs.tags.models.tag import PostTag
    from blogs.users.models.user import User


class Post(BaseModel):
    __tablename__ = "posts"

    # id, created_at, and updated_at are inherited from BaseModel

    # Post title, limited to 100 characters.
    title: Mapped[str] = mapped_column(String(100))

    # Post content, suitable for long articles.
    content: Mapped[str] = mapped_column(Text)

    # Rating can be an integer or None.
    # SQLAlchemy automatically makes this column nullable.
    rating: Mapped[int | None] = mapped_column(default=None)

    # Whether the post is published.
    # New posts are published by default at the ORM level.
    published: Mapped[bool] = mapped_column(default=True)

    # Foreign key referencing the id column in the users table.
    # Since User.id is a UUID (from BaseModel), author_id is UUID.
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    # ORM relationship with the User model.
    # Allows us to access the author object using post.author.
    # back_populates connects this to User.posts.
    author: Mapped[User] = relationship(back_populates="posts")

    # ORM relationship with the Comment model.
    # Allows us to access all comments of a post using post.comments.
    # back_populates connects this to Comment.post.
    comments: Mapped[list[Comment]] = relationship(back_populates="post")

    # ORM relationship with the PostTag junction model.
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="post")
