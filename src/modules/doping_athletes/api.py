from sqlite3 import Connection

from fastapi import APIRouter, Depends
from openpyxl import load_workbook
from starlette.responses import Response

from core.methods import get_connection
from modules.doping_athletes.schemes import Doping

router = APIRouter(prefix='/doping-athletes')

@router.get('/')
def get_doping_athletes(connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM doping_athletes")
    result = cursor.fetchall()

    return {"data": result}
