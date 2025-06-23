from sqlite3 import Connection
from typing_extensions import Annotated

from fastapi import APIRouter, Depends

from core.methods import get_connection
from modules.municipalities.schemes import Municipalities

router = APIRouter()


@router.get('/municipalities')
def get_municipalities(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM municipalities ORDER BY title')
    data = cursor.fetchall()

    return {"data": Municipalities.validate_python(data)}
