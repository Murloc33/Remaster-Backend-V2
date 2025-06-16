from sqlite3 import Connection

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.methods import get_connection
from modules.sports.modules.sports.schemes import Sports

router = APIRouter()


@router.get('/')
def get_sports(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM sports')
    data = cursor.fetchall()

    return {"data": Sports.validate_python(data)}
