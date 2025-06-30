from typing import List, Literal

from pydantic import BaseModel, TypeAdapter


class Discipline(BaseModel):
    id: int
    name: str


Disciplines = TypeAdapter(List[Discipline])


class Content(BaseModel):
    id: int
    name: str


class AdditionalData(BaseModel):
    system_count: Literal['meter', 'second']
    contents: List[Content]


class Sex(BaseModel):
    id: int
    name: str


SexArray = TypeAdapter(List[Sex])
