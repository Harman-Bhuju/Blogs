from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import BaseModel

# Import related models only during static type checking.
# This helps type checkers understand relationship types
# without creating circular imports at runtime.
if TYPE_CHECKING:
    from blogs.comments.models.comment import Comment
    from blogs.posts.models.post import Post


class User(BaseModel):
    __tablename__ = "users"

    # id, created_at, and updated_at are inherited from BaseModel

    # User's name, limited to 100 characters.
    name: Mapped[str] = mapped_column(String(100))

    # User's email, which must be unique.
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # One user can have multiple posts.
    # back_populates connects this relationship to Post.author.
    posts: Mapped[list[Post]] = relationship(back_populates="author")

    # All the comments of a user. This establishes a one-to-many relationship between User and Comment.
    # back_populates connects this relationship to Comment.user.
    comments: Mapped[list[Comment]] = relationship(back_populates="user")
