from datetime import datetime
from sqlite3 import Connection
from typing import Optional, Union

from dateutil.relativedelta import relativedelta
from dateutil.tz import UTC
from fastapi import APIRouter, Depends, Body
from pydantic import AwareDatetime
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.modules.computer_sports.schemes import ComputerSportsData, SubjectsData

router = APIRouter(prefix='/3')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM computer_sport_competition_statuses')
    computer_sports_competition_statuses = cursor.fetchall()

    cursor.execute('SELECT * FROM computer_sport_discipline')
    computer_sports_discipline = cursor.fetchall()

    return JSONResponse(content={"data": ComputerSportsData
        (
        competition_statuses=computer_sports_competition_statuses,
        disciplines=computer_sports_discipline
    ).model_dump()})


@router.post('/data')
def get_data_additional_condition(
        sports_category_id: Annotated[int, Body()],
        competition_status_id: Annotated[int, Body()],
        place: Annotated[int, Body()],
        birth_date: Annotated[AwareDatetime, Body()],
        win_math: Annotated[int, Body()],
        discipline_id: Annotated[int, Body()],
        connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT (is_internally_subject)
        FROM computer_sport
        WHERE competition_status_id = ?
        """,
        (competition_status_id,)
    )

    is_internally_subject = cursor.fetchone()["is_internally_subject"]

    age = relativedelta(datetime.now(tz=UTC), birth_date).years
    if (sports_category_id == 1 and age < 16) or (sports_category_id == 2 and age < 14):
        return {"data": {"is_internally_subject": is_internally_subject, "subjects_data" : []}}

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT subject_from, subject_to
        FROM computer_sport
        WHERE competition_status_id = ?
        AND discipline_id = ? 
        AND ? BETWEEN place_from AND place_to
        AND ? >= win_match
        """,
        (
            competition_status_id, discipline_id, place, win_math
        )
    )

    subject_data = cursor.fetchall()

    return JSONResponse(content={"data" :SubjectsData(is_internally_subject=is_internally_subject,subjects=subject_data).model_dump()})




@router.post('/check-result')
def check_result(
        sports_category_id: Annotated[int, Body()],
        competition_status_id: Annotated[int, Body()],
        place: Annotated[int, Body()],
        birth_date: Annotated[AwareDatetime, Body()],
        win_math: Annotated[int, Body()],
        first_additional: Annotated[bool, Body()],
        second_additional: Annotated[bool, Body()],
        third_additional: Annotated[bool, Body()],

        connection: Annotated[Connection, Depends(get_connection)]
):
    age = relativedelta(datetime.now(tz=UTC), birth_date).years
    if (sports_category_id == 1 and age < 16) or (sports_category_id == 2 and age < 14):
        return {"data": {"is_sports_category_granted": False}}

    cursor = connection.cursor()

    cursor.execute(
        'SELECT * FROM computer_sport WHERE sports_category_id = ? '
        'AND ? BETWEEN place_from AND place_to AND competition_status_id = ? '
        'AND ? >= win_match',
        (
            sports_category_id, place, competition_status_id, win_math
        )
    )

    if (first_additional is None or first_additional == True) or (second_additional is None or second_additional == True) and (third_additional is None or third_additional == True):
        result = len(cursor.fetchall())
        return {"data": {"is_sports_category_granted": result > 0}}

    return {"data": {"is_sports_category_granted": False}}
