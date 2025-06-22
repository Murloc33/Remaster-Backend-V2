from typing import List, Union

from pydantic import TypeAdapter, BaseModel


class Database(BaseModel):
    slug: str
    title: str
    date: str
    file_name: Union[str, None]


Databases = TypeAdapter(List[Database])
