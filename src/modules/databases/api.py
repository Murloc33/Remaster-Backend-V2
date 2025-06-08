import shutil
from datetime import datetime
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body
from openpyxl import load_workbook
from starlette.responses import Response
from typing_extensions import Annotated

from core.methods import get_connection
from modules.databases.schemes import Databases

router = APIRouter(prefix='/databases')


@router.get('/')
def read_database(connection: Annotated[Connection, Depends(get_connection)]):
    cursor = connection.cursor()

    cursor.execute("Select * from databases")
    result = cursor.fetchall()

    return {"data": Databases.validate_python(result)}

def convert_date(original_date: datetime):
    if original_date == None:
        return 'None'
    try:
        return original_date.strftime("%d.%m.%Y")
    except AttributeError:
        return original_date

@router.put('/doping-athletes/upload')
def update_doping_athlete(
    path: Annotated[str, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('DELETE FROM doping_athletes')
    cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = ?', ('doping_athletes',))
    connection.commit()

    wb = load_workbook(path)

    for row in wb["Лист1"].iter_rows(min_row=4, values_only=True):
        if not any(row):
            break

        cursor.execute(
            "INSERT INTO  doping_athletes "
            "(full_name, sport, birth_date, violation_description, disqualification_duration, disqualification_start, disqualification_end)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                row[0], row[2].capitalize(), convert_date(row[1]), row[3], row[4].capitalize(),
                convert_date(row[5]), convert_date(row[6])
            )
        )

    cursor.execute('UPDATE databases SET date = ? WHERE slug = ?', (str(datetime.now().strftime('%d.%m.%Y')), "doping-athletes"))
    connection.commit()

    return Response()


@router.put('/orders/upload')
def update_order(
    path: Annotated[str, Body()],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute("UPDATE databases SET date = ? WHERE slug = ?", (str(datetime.now().strftime('%d.%m.%Y')), "order"))

    destination_path = "../resources/Шаблон_приказа.docx"
    shutil.copy(path, destination_path)

    return Response()
