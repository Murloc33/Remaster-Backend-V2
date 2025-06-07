from sqlite3 import Connection

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.methods import get_connection
from modules.documents.modules.documents.schemes import Document

router = APIRouter()


@router.get('/')
def get_documents(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT id, title FROM documents')
    results = cursor.fetchall()

    return {'data': [Document(**result) for result in results]}
