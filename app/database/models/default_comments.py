from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field
from datetime import datetime


class DefaultCommentsBase(SQLModel):
    author: str = Field(min_length=1)
    text: str = Field(min_length=1)
    group: str | None = Field(None, nullable=True)

    __table_args__ = (UniqueConstraint("text", "group"),)


class DefaultComments(DefaultCommentsBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    changed: datetime = Field(default=None, nullable=True)


class DefaultCommentsUpdate(SQLModel):
    author: Optional[str] = Field(min_length=1)
    text: Optional[str] = Field(min_length=1)
    group: str | None = Field(None)
