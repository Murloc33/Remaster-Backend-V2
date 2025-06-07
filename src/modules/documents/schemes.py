from pydantic import BaseModel


class CreateDocument(BaseModel):
    title: str
    sports_category_id: int


class Document(BaseModel):
    title: str
    sports_category_id: int


class Order(BaseModel):
    path: str
