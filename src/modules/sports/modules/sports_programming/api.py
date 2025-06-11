from datetime import datetime
from sqlite3 import Connection

from dateutil.relativedelta import relativedelta
from dateutil.tz import UTC
from fastapi import APIRouter, Depends, Body
from pydantic import AwareDatetime
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.modules.sports_programming.schemes import SportsProgrammingData

router = APIRouter(prefix='/2')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM sports_programming_competition_statuses')
    sports_programming_competition_statuses = cursor.fetchall()

    return JSONResponse(content={"data": SportsProgrammingData(competition_statuses=sports_programming_competition_statuses).model_dump()})


@router.post('/check-result')
def check_result(
    sports_category_id: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    age = relativedelta(datetime.now(tz=UTC), birth_date).years

    cursor.execute(
        'SELECT * FROM sports_programming WHERE sports_category_id = ? '
        'AND ? BETWEEN place_from AND place_to AND competition_status_id = ? AND ? BETWEEN age_from AND ifnull(age_to, 99999)',
        (
            sports_category_id, place, competition_status_id, age
        )
    )

    result = len(cursor.fetchall())
    return {"data": {"is_sports_category_granted": result > 0}}
