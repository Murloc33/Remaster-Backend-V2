from typing import List, Any, Dict

from pydantic import BaseModel, TypeAdapter


class Athlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality_id: int
    organization_id: int
    is_sports_category_granted: bool
    is_doping_check_passed: bool
    doping_data: Dict[str, Any]
    result_data: Dict[str, Any]


Athletes = TypeAdapter(List[Athlete])
