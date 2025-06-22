from typing import List

from pydantic import BaseModel, TypeAdapter


class Module(BaseModel):
    id: int
    title: str
    sport_id: int


Modules = TypeAdapter(List[Module])
