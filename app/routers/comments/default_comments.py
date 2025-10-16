from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy import desc
from sqlmodel import select, Session

from database.database import get_session
from database.models.default_comments import (
    DefaultComments,
    DefaultCommentsBase,
    DefaultCommentsUpdate,
)

router = APIRouter(tags=["default comments"], prefix="/default_comment")


@router.get("/all", status_code=200)
def get_all_default_comments(
    session: Session = Depends(get_session),
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    contains: Optional[str] = None,
    group: Optional[str] = None,
    limit: Optional[int] = Query(default=50, ge=1),
    offset: Optional[int] = Query(default=0, ge=0),
):
    """Returns list of comments for particular object id"""

    filter_conditions = []
    if created_from:
        filter_conditions.append(DefaultComments.created >= created_from)

    if created_to:
        filter_conditions.append(DefaultComments.created <= created_to)

    if contains:
        filter_conditions.append(
            or_(
                DefaultComments.text.ilike(f"%{contains}%"),  # noqa
                DefaultComments.author.ilike(f"%{contains}%"),  # noqa
                DefaultComments.group.ilike(f"%{contains}%"),  # noqa
            )
        )

    if group:
        filter_conditions.append(DefaultComments.group == group)

    stmt = (
        select(DefaultComments)
        .where(*filter_conditions)
        .order_by(desc(DefaultComments.created))
        .offset(offset)
        .limit(limit)
    )

    comments = session.exec(stmt).all()

    stmt = (
        select([func.count()])
        .select_from(DefaultComments)
        .where(*filter_conditions)
    )
    quantity = session.execute(stmt).first()

    return {"quantity": quantity.count, "comments": comments}


@router.get("/{comment_id}", status_code=200, response_model=DefaultComments)
def get_default_comment_by_id(
    comment_id, session: Session = Depends(get_session)
):
    """Returns comment info"""
    stmt = select(DefaultComments).where(DefaultComments.id == comment_id)
    comment = session.exec(stmt).first()
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )
    return comment


@router.post("/", status_code=201, response_model=DefaultComments)
def create_default_comment(
    comment: DefaultCommentsBase, session: Session = Depends(get_session)
):
    """Creates comment"""
    item = DefaultComments.from_orm(comment)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/{comment_id}", response_model=DefaultComments, status_code=200)
async def update_default_comment(
    comment_id: str,
    comment: DefaultCommentsUpdate,
    session: Session = Depends(get_session),
):
    """Updates comment by comment id"""
    stmt = select(DefaultComments).where(DefaultComments.id == comment_id)
    item = session.exec(stmt).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )

    for attr in comment:
        if attr[1] is not None or attr[0] == "group":
            setattr(item, attr[0], attr[1])
    item.changed = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{comment_id}", status_code=204)
def delete_default_comment_by_id(
    comment_id, session: Session = Depends(get_session)
):
    """Deletes comment by comment_id"""
    stmt = select(DefaultComments).where(DefaultComments.id == comment_id)
    comment = session.exec(stmt).first()
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )
    session.delete(comment)
    session.commit()

    return {"msg": "Comment successfully deleted"}
