import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID4


class MemeBase(BaseModel):
    filename: str = Field(..., max_length=64)
    image_url: str = Field(..., max_length=2096)
    description: Optional[str] = Field(..., max_length=512)
    expires_at: Optional[dt.datetime] = Field(
        ..., default_factory=dt.datetime.now
    )


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    filename: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    expires_at: Optional[dt.datetime] = None


class MemeUpdateDescription(MemeBase):
    description: Optional[str] = None


class MemeRead(MemeBase):
    id: UUID4
