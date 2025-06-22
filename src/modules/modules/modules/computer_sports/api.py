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
from modules.modules.modules.computer_sports.schemes import ComputerSportsData, AdditionalConditions, \
    AdditionalCondition, SubjectType

router = APIRouter(prefix='/4')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM computer_sport_competition_statuses')
    computer_sports_competition_statuses = cursor.fetchall()

    cursor.execute('SELECT * FROM computer_sport_discipline')
    computer_sports_discipline = cursor.fetchall()

    return JSONResponse(
        content={
            "data": ComputerSportsData(
                competition_statuses=computer_sports_competition_statuses,
                disciplines=computer_sports_discipline,
                disciplines_with_mandatory_participation=[1, 5]
            ).model_dump()
        }
    )


@router.post('/additional-conditions')
def get_additional_conditions(
    sports_category_id: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
    discipline_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        "SELECT is_internally_subject FROM computer_sport WHERE competition_status_id = ?",
        (competition_status_id,)
    )
    is_internally_subject = cursor.fetchone()["is_internally_subject"]

    cursor.execute(
        """
        SELECT win_match, subject_from, subject_to
        FROM computer_sport
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sports_category_id = ?
          AND ? BETWEEN place_from AND place_to
          AND NOT (subject_from is NULL AND win_match = 0)
        """,
        (competition_status_id, discipline_id, sports_category_id, place)
    )
    data = cursor.fetchall()

    return JSONResponse(
        content={
            "data": AdditionalConditions(
                is_internally_subject=is_internally_subject,
                additional_conditions=[
                    AdditionalCondition(
                        subject=SubjectType(**value) if value["subject_from"] is not None else None,
                        min_won_matches=value["win_match"] if value["win_match"] != 0 else None,
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
    third_condition: Annotated[Union[bool, None], Body()] = None,
):
    age = relativedelta(datetime.now(tz=UTC), birth_date).years

    if (sports_category_id == 1 and age < 16) or (sports_category_id == 2 and age < 14):
        return {"data": {"is_sports_category_granted": False}}

    if place >= 9 and sports_category_id == 2 and not third_condition:
        return {"data": {"is_sports_category_granted": False}}

    if discipline_id in (1, 5) and not second_condition:
        return {"data": {"is_sports_category_granted": False}}

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT win_match, subject_from, subject_to
        FROM computer_sport
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sports_category_id = ?
          AND ? BETWEEN place_from AND place_to
        """,
        (competition_status_id, discipline_id, sports_category_id, place)
    )
    result = cursor.fetchall()

    if len(result) == 0:
        return {"data": {"is_sports_category_granted": False}}

    for row in result:
        if row['subject_from'] is None and row['win_match'] == 0:
            return {"data": {"is_sports_category_granted": True}}

    if first_condition:
        return {"data": {"is_sports_category_granted": True}}

    return {"data": {"is_sports_category_granted": False}}
