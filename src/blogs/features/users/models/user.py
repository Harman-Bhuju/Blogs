from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models import BaseModel

# TYPE_CHECKING is True only for type linters/IDEs, never at runtime.
# This prevents circular import errors between related models.
if TYPE_CHECKING:
    from blogs.features.comments.models import Comment
    from blogs.features.posts.models import Post


class User(BaseModel):
    __tablename__ = "users"

    # id (UUID), created_at, and updated_at are inherited from BaseModel.
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # 1. One User has Many Posts.
    # back_populates="author" links User.posts <-> Post.author.
    # How to use: user.posts gives a list of all Post objects by this user.
    posts: Mapped[list[Post]] = relationship(back_populates="author")

    # 2. One User has Many Comments.
    # back_populates="user" links User.comments <-> Comment.user.
    # How to use: user.comments gives a list of all Comment objects by this user.
    comments: Mapped[list[Comment]] = relationship(back_populates="user")
