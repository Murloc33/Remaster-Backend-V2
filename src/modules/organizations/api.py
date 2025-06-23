from sqlite3 import Connection
from typing import Annotated

from fastapi import APIRouter, Depends

from core.methods import get_connection
from modules.organizations.schemes import Organizations

router = APIRouter()


@router.get('/organizations')
def get_organizations(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM organizations ORDER BY title')
    data = cursor.fetchall()

    return {"data": Organizations.validate_python(data)}
