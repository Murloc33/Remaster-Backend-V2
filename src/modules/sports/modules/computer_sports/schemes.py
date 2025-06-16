from typing import List

from pydantic import BaseModel


class CompetitionStatus(BaseModel):
    id: int
    name: str

class ComputerSportsData(BaseModel):
    competition_statuses: List[CompetitionStatus]

