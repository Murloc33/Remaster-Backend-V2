import json
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body, Path
from starlette.responses import Response
from typing_extensions import Annotated

from core.methods import get_connection
from modules.documents.modules.file.schemes import Document

router = APIRouter()


@router.post('/file')
def create_document_from_file(
        path: Annotated[str, Body()],
        connection: Annotated[Connection, Depends(get_connection)]
):
    data = json.load(open(path))["data"]

    cursor = connection.cursor()
    cursor.execute('INSERT INTO documents (title, sports_category_id) VALUES (?, ?) RETURNING id',
                   (data['title'], data['sports_category_id']))

    document_id = cursor.fetchone()["id"]

    connection.commit()

    for item in data["athletes"]:
        cursor.execute(
            'INSERT INTO document_athletes (document_id, full_name, birth_date, sport_id, municipality, organization,'
            'is_sports_category_granted, is_doping_check_passed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                document_id, item['full_name'], item['birth_date'], item['sport_id'], item['municipality'],
                item['organization'], item['is_sports_category_granted'], item['is_doping_check_passed']
            )
        )
    connection.commit()

    return Response(status_code=200)


@router.post('/{document_id}/file')
def get_document_to_file(
        document_id: Annotated[int, Path()],
        path: Annotated[str, Body()],
        connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('SELECT title, sports_category_id FROM documents WHERE id = ?', (document_id,))
    document_data = cursor.fetchone()

    cursor.execute('SELECT * FROM sports')
    sports_data = {v['id']: v['name'] for v in cursor.fetchall()}

    cursor.execute('SELECT * FROM document_athletes WHERE document_id = ?', (document_id,))
    athletes_data = cursor.fetchall()

    athletes_data.sort(key=lambda athlete: (sports_data[athlete['sport_id']], athlete['full_name']))

    with open(path, 'w', encoding='utf-8') as file:
        json.dump({"data": Document(**document_data, athletes=athletes_data).model_dump()}, fp=file)

    return Response(status_code=200)
