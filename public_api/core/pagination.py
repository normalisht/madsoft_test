from typing import Generic, List, TypeVar, Type

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

T = TypeVar('T')


class PagedResponseSchema(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]


def paginate(
    page: int,
    size: int,
    items: List[T],
    total,
    response_schema: Type[BaseModel],
) -> PagedResponseSchema[T]:
    return PagedResponseSchema(
        total=total,
        page=page,
        size=size,
        results=[response_schema(**jsonable_encoder(item)) for item in items],
    )
