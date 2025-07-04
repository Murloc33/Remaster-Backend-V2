import json
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body, Path
from starlette.responses import JSONResponse, Response
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
            "(document_id, full_name, birth_date, sport_id, municipality_id, organization_id,"
            " is_sports_category_granted, is_doping_check_passed, doping_data, result_data) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
        ),
        (
            document_id, athlete.full_name, athlete.birth_date, athlete.sport_id,
            athlete.municipality_id, athlete.organization_id,
            athlete.is_sports_category_granted, athlete.is_doping_check_passed,
            json.dumps(athlete.doping_data), json.dumps(athlete.result_data)
        )
    )
    id_ = cursor.fetchone()["id"]
    connection.commit()

    return JSONResponse(content={"data": {'id': id_}})


@router.put('/{document_id}/athletes/file')
def put_athlete_file(
    document_id: Annotated[int, Path()],
    path: Annotated[str, Body(embed=True)],
    connection: Annotated[Connection, Depends(get_connection)]
):
    data = json.load(open(path))["data"]

    cursor = connection.cursor()
    for athlete in data:
        cursor.execute(
            'INSERT INTO document_athletes (document_id, full_name, birth_date, sport_id, municipality_id, organization_id,'
            'is_sports_category_granted, is_doping_check_passed, doping_data, result_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (
                document_id, athlete['full_name'], athlete['birth_date'], athlete['sport_id'], athlete['municipality_id'],
                athlete['organization_id'], athlete['is_sports_category_granted'], athlete['is_doping_check_passed'],
                athlete['doping_data'], athlete['result_data']
            )
        )
    connection.commit()

    return Response()
