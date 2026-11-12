from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# TYPE_CHECKING is True only for type linters/IDEs, never at runtime.
# This prevents circular import errors between related models.
if TYPE_CHECKING:
    from blogs.comments.models.comment import Comment
    from blogs.tags.models.tag import PostTag
    from blogs.users.models.user import User


class Post(BaseModel):
    __tablename__ = "posts"

    # id (UUID), created_at, and updated_at are inherited from BaseModel.
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    rating: Mapped[int | None] = mapped_column(default=None)
    published: Mapped[bool] = mapped_column(server_default=text("true"))

    # Foreign key referencing users.id (UUID).
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    # 1. Many Posts belong to One User (Author).
    # back_populates="posts" links Post.author <-> User.posts.
    # How to use: post.author gives the User object who wrote this post.
    author: Mapped[User] = relationship(back_populates="posts")

    # 2. One Post has Many Comments.
    # back_populates="post" links Post.comments <-> Comment.post.
    # How to use: post.comments gives a list of all Comment objects on this post.
    comments: Mapped[list[Comment]] = relationship(back_populates="post")

    # 3. One Post has Many Tags (via junction table PostTag).
    # back_populates="post" links Post.post_tags <-> PostTag.post.
    # How to use: [pt.tag for pt in post.post_tags] gives the tags on this post.
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="post")
