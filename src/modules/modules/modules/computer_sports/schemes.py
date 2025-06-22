from typing import List, Union

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
    disciplines_with_mandatory_participation: List[int]


class SubjectType(BaseModel):
    subject_from: int
    subject_to: Union[int, None]


class AdditionalCondition(BaseModel):
    subject: Union[SubjectType, None]
    min_won_matches: Union[int, None]


class AdditionalConditions(BaseModel):
    is_internally_subject: bool
    additional_conditions: List[AdditionalCondition]
