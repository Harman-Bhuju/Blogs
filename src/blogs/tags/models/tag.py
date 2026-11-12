from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models.base import BaseModel

# Import related models only during static type checking.
# This prevents circular import errors at runtime while still
# giving your IDE and type checker full autocomplete for relationships.
if TYPE_CHECKING:
    from blogs.posts.models.post import Post


class Tag(BaseModel):
    __tablename__ = "tags"

    # Note: id (UUID), created_at, and updated_at are inherited from BaseModel.

    # Unique tag name (e.g. "python", "fastapi", "webdev").
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # One-to-Many: Tag -> PostTag (Junction Table)
    #
    # How back_populates works:
    #   back_populates="tag" links Tag.post_tags to PostTag.tag.
    #
    # How to get relationship data:
    #   tag = db.query(Tag).filter(Tag.name == "fastapi").first()

    #   # Access all posts that have this tag:
    #   for post_tag in tag.post_tags:
    #       print(post_tag.post.title)
    #
    #   Tip: Eager-load post_tags and the nested post:
    #   from sqlalchemy.orm import selectinload
    #   tag = db.query(Tag).options(selectinload(Tag.post_tags).selectinload(PostTag.post)).first()
    
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="tag")


class PostTag(BaseModel):
    __tablename__ = "post_tags"

    # Junction table linking Posts and Tags (Many-to-Many relationship).
    # Note: id (UUID), created_at, and updated_at are inherited from BaseModel.

    # Foreign keys referencing 'posts.id' and 'tags.id' (both UUIDs).
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"))

    # =========================================================================
    # RELATIONSHIPS & back_populates
    # =========================================================================

    # Many-to-One: PostTag -> Post
    #
    # How back_populates works:
    #   back_populates="post_tags" mirrors Post.post_tags.
    #
    # How to get relationship data:
    #   post_tag = db.query(PostTag).first()
    #   print(post_tag.post.title)
    post: Mapped[Post] = relationship(back_populates="post_tags")

    # Many-to-One: PostTag -> Tag
    #
    # How back_populates works:
    #   back_populates="post_tags" mirrors Tag.post_tags.
    #
    # How to get relationship data:
    #   post_tag = db.query(PostTag).first()
    #   print(post_tag.tag.name)
    tag: Mapped[Tag] = relationship(back_populates="post_tags")
