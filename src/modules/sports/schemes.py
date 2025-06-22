from typing import List

from pydantic import BaseModel, TypeAdapter


class Sports(BaseModel):
    id: int
    name: str


Sports = TypeAdapter(List[Sports])
