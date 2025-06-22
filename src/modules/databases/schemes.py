from typing import List

from pydantic import TypeAdapter, BaseModel


class Database(BaseModel):
    slug: str
    title: str
    date: str
    file_name: str


Databases = TypeAdapter(List[Database])
