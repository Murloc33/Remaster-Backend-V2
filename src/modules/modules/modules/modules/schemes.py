from typing import List

from pydantic import BaseModel, TypeAdapter


class Modules(BaseModel):
    id: int
    title: str
    sport_id: int


Sports = TypeAdapter(List[Modules])
