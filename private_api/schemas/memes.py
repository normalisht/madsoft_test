from pydantic import BaseModel, Field
from pydantic.networks import AnyUrl
from pydantic.types import UUID4


class MemeBase(BaseModel):
    description: str = Field(..., max_length=512)
    image_url: AnyUrl = Field(..., max_length=2096)


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass


class MemeRead(MemeBase):
    id: UUID4
