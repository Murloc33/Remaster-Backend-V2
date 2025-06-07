from sqlite3 import Connection

from fastapi import APIRouter, Depends
from starlette.responses import Response

from modules.athletes.schemes import Athlete, UpdateAthlete
from core.methods import get_connection

router = APIRouter(prefix='/athletes')


@router.get('/{athlete_id}')
def get_athletes(athlete_id: int, connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM document_athletes WHERE id = ?", (athlete_id,))
    athlete = cursor.fetchone()

    return {"data": athlete}


@router.put('/{athlete_id}')
def update_athlete(athlete_id: int, athlete: UpdateAthlete, connection: Connection = Depends(get_connection)):
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
    return Response(status_code=200)


@router.delete('/{athlete_id}')
def delete_athlete(athlete_id: int, connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute("DELETE FROM document_athletes WHERE id = ?", (athlete_id,))
    connection.commit()

    return Response(status_code=200)
