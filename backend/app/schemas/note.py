from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class NoteCreateIn(BaseModel):
    title: str
    content: str


class NoteUpdateIn(BaseModel):
    title: str | None = None
    content: str | None = None
