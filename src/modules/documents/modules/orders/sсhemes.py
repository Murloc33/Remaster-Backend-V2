from pydantic import BaseModel, Field
from typing_extensions import Annotated, List


class Athletes(BaseModel):
    full_name: str
    birth_date: Annotated[str, Field(pattern=r'^\d{2}\.\d{2}\.\d{4}$')]
    municipality: str
    organization: str


class Sport(BaseModel):
    name: str
    athletes: List[Athletes]


class Order(BaseModel):
    sports_category_name: str
    sports: List[Sport]
