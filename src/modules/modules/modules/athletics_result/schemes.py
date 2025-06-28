from typing import List, Union

from pydantic import BaseModel


class Discipline(BaseModel):
    id: int
    name: str

class Disciplines(BaseModel):
    disciplines: List[Discipline]

class SystemCounting(BaseModel):
    id: int
    name: str

class Content(BaseModel):
    id: int
    name: str

class AdditionalData(BaseModel):
    system_count: SystemCounting
    contents: List[Content]

class Sex(BaseModel):
    id: int
    name: str

class Data(BaseModel):
    sex: List[Sex]