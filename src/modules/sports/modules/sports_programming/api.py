from datetime import datetime
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.modules.sports_programming.schemes import SportsProgrammingData

router = APIRouter(prefix='/2')


@router.get('/data')
def get_data(connection: Annotated[Connection, Depends(get_connection)]):
    return JSONResponse(content={"data": SportsProgrammingData().model_dump()})


@router.post('/check-result')
def check_result(
    sports_discipline_id: Annotated[int, Body()],
    sports_category_id: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
    place: Annotated[int, Body()],
    birth_date: Annotated[datetime, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    age = (datetime.now().year - birth_date.year)

    cursor.execute(
        'SELECT * FROM competition_filters_sports_programming WHERE sports_categories_id = ? '
        'AND ? BETWEEN place_to AND place_from AND competition_status_id = ? AND ? BETWEEN age_from AND age_to',
        (
            sports_categories_id, place, competition_status_id, age
        )
    )

    result = len(cursor.fetchall())
    return {"data": {"is_sports_category_granted": result > 0}}
