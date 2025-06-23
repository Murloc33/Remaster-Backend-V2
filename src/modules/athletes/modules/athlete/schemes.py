from typing import Any, Dict

from pydantic import BaseModel


class DopingData(BaseModel):
    full_name: str
    selectId: int


class Athlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality_id: int
    organization_id: int
    is_sports_category_granted: bool
    is_doping_check_passed: bool
    doping_data: DopingData
    result_data: Dict[str, Any]


class UpdateAthlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality_id: int
    organization_id: int
    is_sports_category_granted: bool
    is_doping_check_passed: bool
