from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import BaseModel

if TYPE_CHECKING:
    from blogs.posts.models.post import Post


class Tag(BaseModel):
    __tablename__ = "tags"

    # id, created_at, and updated_at are inherited from BaseModel

    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationship to the PostTag junction table
    post_tags: Mapped[list[PostTag]] = relationship(back_populates="tag")


class PostTag(BaseModel):
    __tablename__ = "post_tags"

    # id, created_at, and updated_at are inherited from BaseModel

    post_id: Mapped[UUID] = mapped_column(ForeignKey("posts.id"))
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("tags.id"))

    # Relationships back to Post and Tag
    post: Mapped[Post] = relationship(back_populates="post_tags")
    tag: Mapped[Tag] = relationship(back_populates="post_tags")
