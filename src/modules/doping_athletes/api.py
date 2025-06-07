from sqlite3 import Connection

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from core.methods import get_connection
from modules.doping_athletes.schemes import DopingAthletes

router = APIRouter(prefix='/doping-athletes')


@router.get('/')
def get_doping_athletes(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM doping_athletes")
    result = cursor.fetchall()

    return {"data": DopingAthletes.validate_python(result)}
