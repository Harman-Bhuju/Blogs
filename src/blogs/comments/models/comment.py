from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# Import related models only during static type checking.
# This prevents circular import errors at runtime while still
# giving your IDE and type checker full autocomplete for relationships.
if TYPE_CHECKING:
    from blogs.posts.models.post import Post
    from blogs.users.models.user import User


class Comment(BaseModel):
    __tablename__ = "comments"

    # Note: id (UUID), created_at, and updated_at are inherited from BaseModel.

    # Comment text body.
    content: Mapped[str] = mapped_column(Text)

    # Foreign keys referencing 'users.id' and 'posts.id' (both UUIDs).
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))

    # =========================================================================
    # RELATIONSHIPS & back_populates
    # =========================================================================

    # 1. Many-to-One: Comment -> User (The commenter)
    #
    # How back_populates works:
    #   back_populates="comments" links Comment.user to User.comments.
    #   If comment.user = current_user, then current_user.comments will
    #   include this comment immediately in Python memory.
    #
    # How to get relationship data:
    #   comment = db.query(Comment).filter(Comment.id == comment_id).first()
    #   # Access the user object who wrote this comment:
    #   print("Author:", comment.user.name, comment.user.email)
    #
    #   Tip: Eager-load the author in a single SQL query:
    #   from sqlalchemy.orm import joinedload
    #   comment = db.query(Comment).options(joinedload(Comment.user)).first()
    user: Mapped[User] = relationship(back_populates="comments")

    # 2. Many-to-One: Comment -> Post (The post being commented on)
    #
    # How back_populates works:
    #   back_populates="comments" connects Comment.post to Post.comments.
    #
    # How to get relationship data:
    #   comment = db.query(Comment).first()
    #   # Access the parent post object:
    #   print("Post Title:", comment.post.title)
    post: Mapped[Post] = relationship(back_populates="comments")
