from datetime import datetime
from sqlite3 import Connection

from dateutil.relativedelta import relativedelta
from dateutil.tz import UTC
from fastapi import APIRouter, Depends, Body
from pydantic import AwareDatetime
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.modules.computer_sports.schemes import ComputerSportsData

router = APIRouter(prefix='/3')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM computer_sport')
    computer_sports_competition_statuses = cursor.fetchall()

    return JSONResponse(content={"data": ComputerSportsData(competition_statuses=computer_sports_competition_statuses).model_dump()})


@router.post('/check-result')
def check_result(
    sports_category_id: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    birth_date: Annotated[AwareDatetime, Body()],
    win_math: Annotated[int, Body()],
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
            sports_category_id, place, competition_status_id,  win_math
        )
    )

    result = len(cursor.fetchall())
    return {"data": {"is_sports_category_granted": result > 0}}
