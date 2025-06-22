import json
from typing import List, Any, Dict, Union

from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated


class CreateDocument(BaseModel):
    title: str
    sports_category_id: int


class DopingData(BaseModel):
    full_name: str
    selectId: Union[int, None]


class Athlete(BaseModel):
    id: int
    full_name: str
    birth_date: str
    sport_id: int
    municipality: str
    organization: str
    is_sports_category_granted: bool
    is_doping_check_passed: bool
    doping_data: Annotated[DopingData, BeforeValidator(lambda x: json.loads(x))]
    result_data: Annotated[Dict[str, Any], BeforeValidator(lambda x: json.loads(x))]


class Document(BaseModel):
    id: int
    title: str
    sports_category_id: int
    athletes: List[Athlete]


class UpdateDocument(BaseModel):
    title: str
    sports_category_id: int
