from typing import List

from pydantic import TypeAdapter


class DopingAthlete:
    id: int
    full_name: str
    sport: str
    birth_date: str
    disqualification_duration: str
    disqualification_start: str
    disqualification_end: str


DopingAthletes = TypeAdapter(List[DopingAthlete])
