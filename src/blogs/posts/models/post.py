from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# Import related models only during static type checking.
# This prevents circular import errors at runtime while still
# giving your IDE and type checker full autocomplete for relationships.
if TYPE_CHECKING:
    from blogs.comments.models.comment import Comment
    from blogs.tags.models.tag import PostTag
    from blogs.users.models.user import User


class Post(BaseModel):
    __tablename__ = "posts"

    # Note: id (UUID), created_at, and updated_at are inherited from BaseModel.

    # Post title, limited to 100 characters.
    title: Mapped[str] = mapped_column(String(100))

    # Post content, suitable for long articles.
    content: Mapped[str] = mapped_column(Text)

    # Optional rating for the post (nullable by default).
    rating: Mapped[int | None] = mapped_column(default=None)

    # Whether the post is published and visible to readers.
    published: Mapped[bool] = mapped_column(default=True)

    # Foreign key referencing the 'id' column in the 'users' table.
    # Since User.id is a UUID (from BaseModel), author_id must also be UUID.
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))


    # 1. Many-to-One: Post -> User (Author)
    #
    # How back_populates works:
    #   back_populates="posts" mirrors User.posts.
    #   Whenever post.author is assigned, SQLAlchemy automatically updates
    #   the author's 'posts' collection in memory.
    #
    # How to get relationship data:
    #   post = db.query(Post).filter(Post.id == post_id).first()
    #   # Get the author user object directly:
    #   print(post.author.name, post.author.email)
    #
    #   Tip: To fetch the post AND its author in a single SQL JOIN:
    #   from sqlalchemy.orm import joinedload
    #   post = db.query(Post).options(joinedload(Post.author)).first()
    author: Mapped[User] = relationship(back_populates="posts")

    # 2. One-to-Many: Post -> Comments
    #
    # How back_populates works:
    #   back_populates="post" links Post.comments to Comment.post.
    #
    # How to get relationship data:
    #   post = db.query(Post).first()
    #   # Access all comments attached to this post:
    #   for comment in post.comments:
    #       print(comment.content, "by user:", comment.user.name)
    #
    #   Tip: Eager-load comments:
    #   from sqlalchemy.orm import selectinload
    #   post = db.query(Post).options(selectinload(Post.comments)).first()
    comments: Mapped[list[Comment]] = relationship(back_populates="post")

    # 3. One-to-Many: Post -> PostTag (Junction Table)
    #
    # How back_populates works:
    #   back_populates="post" connects Post.post_tags to PostTag.post.
    #   PostTag holds the link between Post and Tag.
    #
    # How to get relationship data:
    #   post = db.query(Post).first()
    #   # Access all tags on this post through the junction table:
    #   for post_tag in post.post_tags:
    #       print("Tag name:", post_tag.tag.name)
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="post")
