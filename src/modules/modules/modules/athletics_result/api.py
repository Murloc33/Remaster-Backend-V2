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
from modules.modules.modules.athletics_result.schemes import Disciplines, AdditionalData, Data

router = APIRouter(prefix='/1')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM sex')
    sex = cursor.fetchall()

    return JSONResponse(
        content={
            "data": Data(
                sex=sex
            ).model_dump()
        }
    )


@router.post('/additional-conditions-discipline')
def get_additional_conditions_discipline(
        sex_id: Annotated[int, Body(embed=True)],
        connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('SELECT id, name FROM athletics_result_disciplines WHERE sex_id = ?', (sex_id,))
    disciplines = cursor.fetchall()

    return JSONResponse(
        content={
            "data": Disciplines(
                disciplines=disciplines
            ).model_dump()
        }
    )


@router.post('/additional-conditions')
def get_additional_conditions(
        discipline_id: Annotated[int, Body()],
        sport_category_id: Annotated[int, Body()],
        connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        'SELECT system_counting_id as id, system_counting.name FROM athletics_result_disciplines JOIN system_counting ON system_counting_id=system_counting.id WHERE athletics_result_disciplines.id = ?',
        (discipline_id,))
    system_count = cursor.fetchone()

    cursor.execute("""
                   SELECT discipline_content_id as id, athletics_result_discipline_contents.name
                   FROM athletics_result
                            JOIN athletics_result_discipline_contents
                                 ON discipline_content_id = athletics_result_discipline_contents.id
                   WHERE athletics_result.discipline_id = ?
                       AND athletics_result.sport_category_id = ?
                   """,
                   (
                       discipline_id,
                       sport_category_id,
                   )
    )
    contents = cursor.fetchall()

    return JSONResponse(
        content={
            "data": AdditionalData(
                system_count=system_count,
                contents=contents
            ).model_dump()
        }
    )


@router.post('/check-result')
def check_result(
        sports_category_id: Annotated[int, Body()],
        birth_date: Annotated[AwareDatetime, Body()],
        discipline_id: Annotated[int, Body()],
        content_id: Annotated[int, Body()],
        result: Annotated[int, Body()],
        connection: Annotated[Connection, Depends(get_connection)],
        first_condition: Annotated[Union[bool, None], Body()] = None,
):
    age = relativedelta(datetime.now(tz=UTC), birth_date).years

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM athletics_result
        WHERE discipline_id = ?
          AND discipline_content_id = ?
          AND sport_category_id = ?
          AND ? BETWEEN age_from AND age_to
        """,
        (discipline_id, content_id, sports_category_id, age)
    )

    result = cursor.fetchall()

    if len(result) == 0:
        return {"data": {"is_sports_category_granted": False}}

    if first_condition:
        return {"data": {"is_sports_category_granted": True}}

    return {"data": {"is_sports_category_granted": False}}
