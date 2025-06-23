from typing import List, Any

from pydantic import BaseModel


class Athlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality_id: int
    organization_id: int
    is_sports_category_granted: bool
    is_doping_check_passed: bool
    doping_data: Any
    result_data: Any


class Document(BaseModel):
    title: str
    sports_category_id: int
    athletes: List[Athlete]
