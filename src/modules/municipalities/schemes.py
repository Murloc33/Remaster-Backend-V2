from typing import List

from pydantic import BaseModel, TypeAdapter


class Municipality(BaseModel):
    id: int
    title: str


Municipalities = TypeAdapter(List[Municipality])
