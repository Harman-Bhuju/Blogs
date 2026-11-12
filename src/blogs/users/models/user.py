from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# Import related models only during static type checking.
# This prevents circular import errors at runtime while still
# giving your IDE and type checker full autocomplete for relationships.
if TYPE_CHECKING:
    from blogs.comments.models.comment import Comment
    from blogs.posts.models.post import Post


class User(BaseModel):
    __tablename__ = "users"

    # Note: id (UUID), created_at, and updated_at are inherited from BaseModel.

    # User's display name, max 100 characters.
    name: Mapped[str] = mapped_column(String(100))

    # User's unique email address.
    email: Mapped[str] = mapped_column(String(255), unique=True)

    # 1. One-to-Many: User -> Posts
    #
    # How back_populates works:
    #   back_populates="author" links this attribute (User.posts) to the
    #   'author' attribute on the Post model (Post.author).
    #   Because of this two-way link:
    #     - user.posts.append(new_post) automatically sets new_post.author = user.
    #     - new_post.author = user automatically adds new_post to user.posts.
    #
    # How to get relationship data:
    #   user = db.query(User).filter(User.id == user_id).first()
    #   # Access all posts written by this user:
    #   for post in user.posts:
    #       print(post.title, post.content)
    #
    #   Tip: To avoid N+1 query overhead, eager-load posts in one query:
    #   from sqlalchemy.orm import selectinload
    #   user = db.query(User).options(selectinload(User.posts)).first()
    posts: Mapped[list[Post]] = relationship(back_populates="author")

    # 2. One-to-Many: User -> Comments
    #
    # How back_populates works:
    #   back_populates="user" links User.comments to Comment.user.
    #   Both sides stay in sync in Python memory.
    #
    # How to get relationship data:
    #   user = db.query(User).first()
    #   # Access all comments written by this user:
    #   for comment in user.comments:
    #       print(comment.content, "on post:", comment.post_id)
    comments: Mapped[list[Comment]] = relationship(back_populates="user")
