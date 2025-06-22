from typing import List

from pydantic import BaseModel


class CompetitionStatus(BaseModel):
    id: int
    name: str

class Discipline(BaseModel):
    id: int
    name: str


class SportsProgrammingData(BaseModel):
    competition_statuses: List[CompetitionStatus]
    disciplines: List[Discipline]
    