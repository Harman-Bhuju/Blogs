from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import BaseModel

# Import related models only during static type checking.
# This helps type checkers understand relationship types
# without creating circular imports at runtime.
if TYPE_CHECKING:
    from blogs.posts.models.post import Post
    from blogs.users.models.user import User


class Comment(BaseModel):
    __tablename__ = "comments"

    # id, created_at, and updated_at are inherited from BaseModel

    content: Mapped[str] = mapped_column(Text)

    # Foreign keys referencing User and Post (both UUIDs from BaseModel)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))

    # ORM relationship with the User model.
    # Allows us to access the author object using comment.user.
    # back_populates connects this to User.comments.
    user: Mapped[User] = relationship(back_populates="comments")

    # ORM relationship with the Post model.
    # Allows us to access the post object using comment.post.
    # back_populates connects this to Post.comments.
    post: Mapped[Post] = relationship(back_populates="comments")
