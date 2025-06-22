from datetime import datetime
from sqlite3 import Connection
from typing import Union

from dateutil.relativedelta import relativedelta
from dateutil.tz import UTC
from fastapi import APIRouter, Depends, Body
from pydantic import AwareDatetime
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.modules.modules.athletics_place.schemes import AthleticsPlaceData, AdditionalConditions, \
    AdditionalCondition

router = APIRouter(prefix='/2')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM athletics_place_competition_statuses')
    computer_sports_competition_statuses = cursor.fetchall()

    cursor.execute('SELECT * FROM athletics_place_disciplines')
    computer_sports_discipline = cursor.fetchall()

    return JSONResponse(
        content={
            "data": AthleticsPlaceData(
                competition_statuses=computer_sports_competition_statuses,
                disciplines=computer_sports_discipline,
                disciplines_with_minimum_number_of_participants=[10, 11, 12]
            ).model_dump()
        }
    )


@router.post('/additional-conditions')
def get_additional_conditions(
    sports_category_id: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    competition_status_id: Annotated[int, Body()],
    discipline_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    connection: Annotated[Connection, Depends(get_connection)],
):
    cursor = connection.cursor()

    age = datetime.now(tz=UTC).year - birth_date.year

    cursor.execute(
        """
        SELECT min_participants, subject_from
        FROM athletics_place
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sport_category_id = ?
          AND ? BETWEEN place_from AND place_to
          AND ? BETWEEN age_from AND age_to
          AND NOT (subject_from is NULL AND min_participants is NULL)
        """,
        (competition_status_id, discipline_id, sports_category_id, place, age)
    )
    data = cursor.fetchall()

    return JSONResponse(
        content={
            "data": AdditionalConditions(
                additional_conditions=[
                    AdditionalCondition(
                        subject_from= value["subject_from"] if value["subject_from"] is not None else None,
                        min_participants= value["min_participants"] if value["min_participants"] != 0 else None,
                    ) for value in data
                ]
            ).model_dump()
        }
    )


@router.post('/check-result')
def check_result(
    sports_category_id: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    competition_status_id: Annotated[int, Body()],
    discipline_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    connection: Annotated[Connection, Depends(get_connection)],
    first_condition: Annotated[Union[bool, None], Body()] = None,
    second_condition: Annotated[Union[bool, None], Body()] = None,
):
    age = datetime.now(tz=UTC).year - birth_date.year

    if discipline_id in (10, 11, 12) and sports_category_id == 1 and not second_condition:
        return {"data": {"is_sports_category_granted": False}}

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT subject_from, min_participants
        FROM athletics_place
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sport_category_id = ?
          AND ? BETWEEN place_from AND place_to
          AND ? BETWEEN age_from AND age_to
        """,
        (competition_status_id, discipline_id, sports_category_id, place, age)
    )
    result = cursor.fetchall()

    if len(result) == 0:
        return {"data": {"is_sports_category_granted": False}}

    for row in result:
        if row['subject_from'] is None and row['min_participants'] is None:
            return {"data": {"is_sports_category_granted": True}}

    if first_condition:
        return {"data": {"is_sports_category_granted": True}}

    return {"data": {"is_sports_category_granted": False}}
