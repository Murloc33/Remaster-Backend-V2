from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body, Path
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.documents.modules.athletes.schemes import CreateAthlete

router = APIRouter()


@router.post('/{document_id}/athletes')
def create_athlete(
    document_id: Annotated[int, Path()],
    athlete: Annotated[CreateAthlete, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        (
            "INSERT INTO document_athletes "
            "(document_id, full_name, birth_date, sport_id, municipality, organization,"
            " is_sports_category_granted, is_doping_check_passed) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
        ),
        (
            document_id, athlete.full_name, athlete.birth_date, athlete.sport_id,
            athlete.municipality, athlete.organization,
            athlete.is_sports_category_granted, athlete.is_doping_check_passed
        )
    )
    id_ = cursor.fetchone()["id"]
    connection.commit()

    return JSONResponse(content={"data": {'id': id_}})
