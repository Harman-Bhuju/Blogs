from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# TYPE_CHECKING is True only for type linters/IDEs, never at runtime.
# This prevents circular import errors between related models.
if TYPE_CHECKING:
    from blogs.posts.models.post import Post
    from blogs.users.models.user import User


class Comment(BaseModel):
    __tablename__ = "comments"

    # id (UUID), created_at, and updated_at are inherited from BaseModel.
    content: Mapped[str] = mapped_column(Text)

    # Foreign keys referencing users.id and posts.id (both UUIDs).
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))

    # 1. Many Comments belong to One User.
    # back_populates="comments" links Comment.user <-> User.comments.
    # How to use: comment.user gives the User object who wrote this comment.
    user: Mapped[User] = relationship(back_populates="comments")

    # 2. Many Comments belong to One Post.
    # back_populates="comments" links Comment.post <-> Post.comments.
    # How to use: comment.post gives the Post object this comment belongs to.
    post: Mapped[Post] = relationship(back_populates="comments")
