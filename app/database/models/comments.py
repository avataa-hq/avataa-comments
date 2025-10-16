from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class CommentsBase(SQLModel):
    author: str = Field(min_length=1)
    text: str = Field(min_length=1)
    object_id: int = Field(nullable=False, ge=0)


class Comments(CommentsBase, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    created: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    changed: datetime = Field(default=None, nullable=True)


class CommentsUpdate(SQLModel):
    author: Optional[str] = Field(min_length=1)
    text: Optional[str] = Field(min_length=1)
    object_id: Optional[int] = Field(nullable=False, ge=0)
