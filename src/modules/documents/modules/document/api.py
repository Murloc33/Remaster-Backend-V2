from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body, Path
from starlette.responses import Response, JSONResponse
from typing_extensions import Annotated

from core.methods import get_connection
from modules.documents.modules.document.schemes import CreateDocument, Document, UpdateDocument

router = APIRouter()


@router.post('/')
def create_document(
    document: Annotated[CreateDocument, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        'INSERT INTO documents (title, sports_category_id) VALUES (?, ?) RETURNING id',
        (document.title, document.sports_category_id)
    )

    id_ = cursor.fetchone()["id"]
    connection.commit()

    return JSONResponse(content={"data": {'id': id_}})


@router.get('/{document_id}')
def get_document(
    document_id: Annotated[int, Path()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM documents WHERE id = ?', (document_id,))
    document_data = cursor.fetchone()

    cursor.execute('SELECT * FROM document_athletes WHERE document_id = ? ORDER BY created_at', (document_id,))
    athletes_data = cursor.fetchall()

    return JSONResponse(content={"data": Document(**document_data, athletes=athletes_data).model_dump()})


@router.put('/{document_id}')
def update_document(
    document_id: Annotated[int, Path()],
    document: Annotated[UpdateDocument, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE documents SET title = ?, sports_category_id = ? WHERE id = ?",
        (document.title, document.sports_category_id, document_id)
    )
    connection.commit()

    return Response()


@router.delete('/{document_id}')
def delete_document(
    document_id: Annotated[int, Path()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('DELETE FROM document_athletes WHERE document_id = ?', (document_id,))
    cursor.execute('DELETE FROM documents WHERE id = ?', (document_id,))
    connection.commit()

    return Response()
