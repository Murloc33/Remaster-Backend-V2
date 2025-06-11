from typing import List

from pydantic import BaseModel


class SportDiscipline(BaseModel):
    id: int
    name: str


class CompetitionStatus(BaseModel):
    id: int
    name: str


class SportsProgrammingData(BaseModel):
    sports_disciplines: List[SportDiscipline]
    competition_statuses: List[CompetitionStatus]
