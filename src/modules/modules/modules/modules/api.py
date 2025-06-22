from sqlite3 import Connection

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.methods import get_connection
from modules.modules.modules.modules.schemes import Modules

router = APIRouter()


@router.get('/')
def get_modules(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM modules ORDER BY title ASC')
    data = cursor.fetchall()

    return {"data": Modules.validate_python(data)}
