from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.errors import ApiError
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreateIn, NoteOut, NoteUpdateIn


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteOut])
def list_notes(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notes = db.scalars(
        select(Note)
        .where(Note.user_id == user.id)
        .order_by(Note.updated_at.desc(), Note.created_at.desc())
    ).all()
    return notes


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: NoteCreateIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = Note(user_id=user.id, title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def _get_owned_note(db: Session, *, note_id: UUID, user_id: UUID) -> Note:
    note = db.scalar(select(Note).where(Note.id == note_id, Note.user_id == user_id))
    if note is None:
        raise ApiError(status_code=404, code="note_not_found", message="Note not found")
    return note


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _get_owned_note(db, note_id=note_id, user_id=user.id)


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: UUID,
    payload: NoteUpdateIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    note = _get_owned_note(db, note_id=note_id, user_id=user.id)

    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content

    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = _get_owned_note(db, note_id=note_id, user_id=user.id)
    db.delete(note)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
