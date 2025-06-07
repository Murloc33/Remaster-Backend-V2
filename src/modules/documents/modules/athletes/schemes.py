from pydantic import BaseModel


class CreateAthlete(BaseModel):
    full_name: str
    birth_date: str
    sport_id: int
    municipality: str
    organization: str
    is_sports_category_granted: bool
    is_doping_check_passed: bool
