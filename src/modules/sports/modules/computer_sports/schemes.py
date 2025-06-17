from typing import List, AnyStr, Optional

from pydantic import BaseModel


class CompetitionStatus(BaseModel):
    id: int
    name: str

class Discipline(BaseModel):
    id: int
    name: str

class ComputerSportsData(BaseModel):
    competition_statuses: List[CompetitionStatus]
    disciplines: List[Discipline]

class SubjectData(BaseModel):
    subject_from: int
    subject_to: Optional[int]

class SubjectsData(BaseModel):
    is_internally_subject: bool
    subjects: List[SubjectData]

