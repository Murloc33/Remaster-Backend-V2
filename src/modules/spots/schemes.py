from typing import List

from pydantic import BaseModel, TypeAdapter


class Sport(BaseModel):
    id: int
    name: str

Sports = TypeAdapter(List[Sport])
