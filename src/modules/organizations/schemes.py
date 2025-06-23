from typing import List

from pydantic import BaseModel, TypeAdapter


class Organization(BaseModel):
    id: int
    title: str
    sport_id: int


Organizations = TypeAdapter(List[Organization])
