from typing import List

from pydantic import TypeAdapter, BaseModel


class Database(BaseModel):
    slug: str
    title: str
    date: str


Databases = TypeAdapter(List[Database])
