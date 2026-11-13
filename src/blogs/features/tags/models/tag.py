from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blogs.common.models import BaseModel

# TYPE_CHECKING is True only for type linters/IDEs, never at runtime.
# This prevents circular import errors between related models.
if TYPE_CHECKING:
    from blogs.features.posts.models import Post


class Tag(BaseModel):
    __tablename__ = "tags"

    # id (UUID), created_at, and updated_at are inherited from BaseModel.
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # One Tag belongs to Many Posts (via junction table PostTag).
    # back_populates="tag" links Tag.post_tags <-> PostTag.tag.
    # How to use: [pt.post for pt in tag.post_tags] gives all posts with this tag.
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="tag")


class PostTag(BaseModel):
    __tablename__ = "post_tags"

    # Junction table linking Posts and Tags (Many-to-Many).
    # id (UUID), created_at, and updated_at are inherited from BaseModel.
    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"))

    # Links junction row back to Post.
    # back_populates="post_tags" links PostTag.post <-> Post.post_tags.
    # How to use: post_tag.post gives the related Post object.
    post: Mapped[Post] = relationship(back_populates="post_tags")

    # Links junction row back to Tag.
    # back_populates="post_tags" links PostTag.tag <-> Tag.post_tags.
    # How to use: post_tag.tag gives the related Tag object.
    tag: Mapped[Tag] = relationship(back_populates="post_tags")
