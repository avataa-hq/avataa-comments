from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from sqlalchemy import func, or_
from sqlalchemy import desc
from sqlmodel import select, Session

from database.database import get_session
from database.models.comments import Comments, CommentsBase, CommentsUpdate

router = APIRouter(tags=["comments"], prefix="/comment")


@router.get("/{comment_id}", status_code=200, response_model=Comments)
def get_comment_by_id(comment_id, session: Session = Depends(get_session)):
    """Returns comment info"""
    stmt = select(Comments).where(Comments.id == comment_id)
    comment = session.exec(stmt).first()
    print(comment)
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )
    return comment


@router.post("/{object_id}", status_code=201, response_model=Comments)
def create_comment_for_particular_object_id(
    comment: CommentsBase, session: Session = Depends(get_session)
):
    """Creates comment"""
    item = Comments.from_orm(comment)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/{object_id}/all", status_code=200)
def get_all_comment_by_object_id(
    object_id: int,
    session: Session = Depends(get_session),
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    contains: Optional[str] = None,
    limit: Optional[int] = Query(default=50, gt=-1),
    offset: Optional[int] = Query(default=0, gt=-1),
):
    """Returns list of comments for particular object id"""

    filter_conditions = []
    if created_from:
        filter_conditions.append(Comments.created >= created_from)

    if created_to:
        filter_conditions.append(Comments.created <= created_to)

    if contains:
        filter_conditions.append(
            or_(
                Comments.text.ilike(f"%{contains}%"),
                Comments.author.ilike(f"%{contains}%"),
            )
        )

    stmt = (
        select(Comments)
        .where(Comments.object_id == object_id, *filter_conditions)
        .order_by(desc(Comments.created))
        .offset(offset)
        .limit(limit)
    )

    comments = session.exec(stmt).all()

    stmt = (
        select([func.count()])
        .select_from(Comments)
        .where(Comments.object_id == object_id, *filter_conditions)
    )
    quantity = session.execute(stmt).first()

    return {"quantity": quantity.count, "comments": comments}


@router.patch("/{comment_id}", response_model=Comments, status_code=200)
async def update_comment(
    comment_id: str,
    comment: CommentsUpdate,
    session: Session = Depends(get_session),
):
    """Updates comment by comment id"""
    stmt = select(Comments).where(Comments.id == comment_id)
    item = session.exec(stmt).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )

    for attr in comment:
        if attr[1] is not None:
            setattr(item, attr[0], attr[1])
    item.changed = datetime.utcnow()
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{comment_id}", status_code=204)
def delete_comment_by_id(comment_id, session: Session = Depends(get_session)):
    """Deletes comment by comment_id"""
    stmt = select(Comments).where(Comments.id == comment_id)
    comment = session.exec(stmt).first()
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id = {comment_id} does not exist.",
        )
    session.delete(comment)
    session.commit()

    return {"msg": "Comment successfully deleted"}
