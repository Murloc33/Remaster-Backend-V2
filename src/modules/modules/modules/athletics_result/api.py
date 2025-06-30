from datetime import datetime
from sqlite3 import Connection
from typing import Union

from dateutil.tz import UTC
from fastapi import APIRouter, Depends, Body
from pydantic import AwareDatetime
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.modules.modules.athletics_result.schemes import Disciplines, AdditionalData, SexArray

router = APIRouter(prefix='/1')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM sex')
    sex = cursor.fetchall()

    return {"data": SexArray.validate_python(sex)}


@router.post('/additional-conditions-discipline')
def get_additional_conditions_discipline(
    sex_id: Annotated[int, Body(embed=True)],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('SELECT id, name FROM athletics_result_disciplines WHERE sex_id = ?', (1,))
    disciplines = cursor.fetchall()

    return {"data": Disciplines.validate_python(disciplines)}


@router.post('/additional-conditions')
def get_additional_conditions(
    discipline_id: Annotated[int, Body()],
    sport_category_id: Annotated[int, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT system_counting_id as id
        FROM athletics_result_disciplines
                 JOIN system_counting ON system_counting_id = system_counting.id
        WHERE athletics_result_disciplines.id = ?
        """,
        (discipline_id,)
    )
    system_count_id = cursor.fetchone()['id']

    cursor.execute(
        """
        SELECT discipline_content_id as id, athletics_result_discipline_contents.name
        FROM athletics_result
                 JOIN athletics_result_discipline_contents
                      ON discipline_content_id = athletics_result_discipline_contents.id
        WHERE athletics_result.discipline_id = ?
          AND athletics_result.sport_category_id = ?
        """,
        (discipline_id, sport_category_id)
    )
    contents = cursor.fetchall()

    return JSONResponse(
        content={
            "data": (
                AdditionalData(
                    system_count='second' if system_count_id == 1 else 'meter',
                    contents=contents
                ).model_dump()
            )
        }
    )


@router.post('/check-result')
def check_result(
    sports_category_id: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    discipline_id: Annotated[int, Body()],
    result: Annotated[float, Body()],
    first_condition: Annotated[Union[bool], Body()],
    connection: Annotated[Connection, Depends(get_connection)],
    content_id: Annotated[Union[int, None], Body()] = None
):
    if not first_condition:
        return {"data": {"is_sports_category_granted": True}}

    age = datetime.now(tz=UTC).year - birth_date.year

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM athletics_result
                 JOIN athletics_result_disciplines ON athletics_result.discipline_id = athletics_result_disciplines.id
        WHERE discipline_id = ?
          AND discipline_content_id = ?
          AND sport_category_id = ?
          AND ? BETWEEN age_from AND age_to
          AND ((athletics_result_disciplines.system_counting_id = 1 AND athletics_result.min_result >= ?) OR
               (athletics_result_disciplines.system_counting_id = 2 AND athletics_result.min_result <= ?))
        """,
        (discipline_id, content_id or 52, sports_category_id, age, result, result)
    )

    result = cursor.fetchall()

    if len(result) == 0:
        return {"data": {"is_sports_category_granted": False}}

    return {"data": {"is_sports_category_granted": True}}
