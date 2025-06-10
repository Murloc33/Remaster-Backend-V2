from datetime import datetime
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.schemes import Sports

router = APIRouter(prefix='/sports')


@router.get('/')
def get_sports(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM sports')
    data = cursor.fetchall()

    return {"data": Sports.validate_python(data)}


@router.post('/2/check-result')
def check_result(
    sports_categories_id: Annotated[int, Body(embed=True)],
    place: Annotated[int, Body()],
    competition_status_id: Annotated[int, Body()],
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
    return result > 0
