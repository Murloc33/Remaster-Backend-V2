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
from modules.sports.modules.computer_sports.schemes import ComputerSportsData, AdditionalConditionsType, SubjectsType

router = APIRouter(prefix='/3')


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
        SELECT win_match
        FROM computer_sport
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sports_category_id = ?
          AND ? BETWEEN place_from AND place_to
        """,
        (competition_status_id, discipline_id, sports_category_id, place)
    )
    min_won_match = cursor.fetchone()["win_match"]

    cursor.execute(
        """
        SELECT subject_from, subject_to
        FROM computer_sport
        WHERE competition_status_id = ?
          AND discipline_id = ?
          AND sports_category_id = ?
          AND ? BETWEEN place_from AND place_to
          AND subject_from IS NOT NULL
        """,
        (competition_status_id, discipline_id, sports_category_id, place)
    )
    subject_data = cursor.fetchall()

    return JSONResponse(
        content={
            "data": AdditionalConditionsType(
                subjects=SubjectsType(
                    is_internally_subject=is_internally_subject,
                    subjects=subject_data
                ),
                min_won_matches=min_won_match
            ).model_dump()
        }
    )


@router.post('/check-result')
def check_result(
    sports_category_id: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    win_math: Annotated[int, Body()],
    discipline_id: Annotated[int, Body()],
    connection: Annotated[Connection, Depends(get_connection)],
    first_additional: Annotated[Union[bool, None], Body()] = None,
    second_additional: Annotated[Union[bool, None], Body()] = None,
    third_additional: Annotated[Union[bool, None], Body()] = None,
):
    age = relativedelta(datetime.now(tz=UTC), birth_date).years
    if (sports_category_id == 1 and age < 16) or (sports_category_id == 2 and age < 14):
        return {"data": {"is_sports_category_granted": False}}

    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM computer_sport WHERE sports_category_id = ? '
        'AND ? BETWEEN place_from AND place_to AND competition_status_id = ? '
        'AND ? >= win_match AND discipline_id = ?',
        (
            sports_category_id, place, competition_status_id, win_math, discipline_id
        )
    )

    if (first_additional is None or first_additional == True) or (second_additional is None or second_additional == True) and (
        third_additional is None or third_additional == True):
        result = len(cursor.fetchall())
        return {"data": {"is_sports_category_granted": result > 0}}

    return {"data": {"is_sports_category_granted": False}}
