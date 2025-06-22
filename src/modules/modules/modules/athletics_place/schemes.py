from typing import List, Union

from pydantic import BaseModel


class CompetitionStatus(BaseModel):
    id: int
    name: str


class Discipline(BaseModel):
    id: int
    name: str


class AthleticsPlaceData(BaseModel):
    competition_statuses: List[CompetitionStatus]
    disciplines: List[Discipline]
    disciplines_with_minimum_number_of_participants_participation: List[int]


class SubjectType(BaseModel):
    subject_from: int
    subject_to: Union[int, None]


class AdditionalCondition(BaseModel):
    subject_from: Union[int, None]
    min_participants: Union[int, None]


class AdditionalConditions(BaseModel):
    additional_conditions: List[AdditionalCondition]
