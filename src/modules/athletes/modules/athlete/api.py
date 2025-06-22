import json
from sqlite3 import Connection
from typing import Any, Literal

from fastapi import APIRouter, Depends, Path, Body
from starlette.responses import Response, JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.athletes.modules.athlete.schemes import UpdateAthlete, Athlete

router = APIRouter()


# @router.get('/{athlete_id}')
# def get_athletes(
#     athlete_id: Annotated[int, Path()],
#     connection: Annotated[Connection, Depends(get_connection)]
# ):
#     cursor = connection.cursor()
#
#     cursor.execute("SELECT * FROM document_athletes WHERE id = ?", (athlete_id,))
#     athlete = cursor.fetchone()
#
#     return JSONResponse(content={"data": Athlete(**athlete).model_dump()})
#

@router.put('/{athlete_id}')
def update_athlete(
    athlete_id: Annotated[int, Path()],
    athlete: Annotated[UpdateAthlete, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        (
            "UPDATE document_athletes SET "
            "full_name = ?, birth_date = ?, sport_id = ?, municipality = ?,"
            "organization = ?, is_sports_category_granted = ?, is_doping_check_passed = ?"
            "WHERE id = ?"
        ),
        (
            athlete.full_name, athlete.birth_date, athlete.sport_id,
            athlete.municipality, athlete.organization, athlete.is_sports_category_granted,
            athlete.is_doping_check_passed, athlete_id
        )
    )

    connection.commit()
    return Response()


@router.delete('/{athlete_id}')
def delete_athlete(
    athlete_id: Annotated[int, Path()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM document_athletes WHERE id = ?", (athlete_id,))
    connection.commit()

    return Response()


@router.get('/{athlete_id}/{slug}')
def get_checker_data(
    athlete_id: Annotated[int, Path()],
    slug: Annotated[Literal['doping', 'result'], Path()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT {slug}_data FROM document_athletes WHERE id = ?",
        (athlete_id,)
    )
    connection.commit()

    data = cursor.fetchone()

    if not data or not data[f'{slug}_data']:
        return {"data": None}

    return {"data": json.loads(data[f'{slug}_data'])}


@router.put('/{athlete_id}/{slug}')
def update_checker_data(
    athlete_id: Annotated[int, Path()],
    slug: Annotated[Literal['doping', 'result'], Path()],
    data: Annotated[Any, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        f"UPDATE document_athletes SET {slug}_data = ? WHERE id = ?",
        (json.dumps(data), athlete_id)
    )
    connection.commit()

    return Response()

