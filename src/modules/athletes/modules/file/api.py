import json
from sqlite3 import Connection
from typing import List

from fastapi import APIRouter, Depends, Body
from starlette.responses import Response
from typing_extensions import Annotated

from core.methods import get_connection
from modules.athletes.modules.file.schemes import Athletes

router = APIRouter()

@router.post('/file')
def get_athletes_to_file(
        athlete_ids: Annotated[List[int], Body()],
        path: Annotated[str, Body()],
        connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()


    placeholders = ','.join(['?'] * len(athlete_ids))
    query = f"SELECT * FROM document_athletes WHERE id IN ({placeholders})"
    cursor.execute(query, athlete_ids)
    athlete_data = cursor.fetchall()

    with open(path, 'w', encoding='utf-8') as file:
        json.dump({"data": [v.model_dump() for v in Athletes.validate_python(athlete_data)]}, fp=file)

    return Response(status_code=200)





