from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Base is the parent class used by every SQLAlchemy model.
#
# Any class that inherits from Base becomes known to SQLAlchemy
# as a database model.
class Base(DeclarativeBase):
    pass


# BaseModel contains columns that should be common
# to most of our database models.
#
# __abstract__ = True means SQLAlchemy will NOT create
# a table called "base_models".
#
# Instead, its columns are inherited by classes such as:
#
#     User(BaseModel)
#     Post(BaseModel)
#     Comment(BaseModel)
#     Tag(BaseModel)
class BaseModel(Base):
    __abstract__ = True

    # UUID = the Python type of our ID.
    #
    # uuid4 = generates a random UUID when a new object
    # is created.
    #
    # primary_key=True means this uniquely identifies
    # each row in the table.
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    # Automatically stores when the row was created.
    #
    # server_default=func.now() means PostgreSQL generates
    # the timestamp when the row is inserted.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Stores when the row was last updated.
    #
    # onupdate=func.now() tells SQLAlchemy to update
    # this timestamp when the row is changed.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
