from typing import List

from pydantic import BaseModel


class CreateDocument(BaseModel):
    title: str
    sports_category_id: int


class Athlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality: str
    organization: str
    is_sports_category_granted: bool
    is_doping_check_passed: bool


class Document(BaseModel):
    id: str
    title: str
    sports_category_id: int
    athletes: List[Athlete]


class UpdateDocument(BaseModel):
    title: str
    sports_category_id: int
