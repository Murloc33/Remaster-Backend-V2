import shutil
from datetime import datetime
from sqlite3 import Connection

from fastapi import APIRouter, Depends, Body
from openpyxl import load_workbook
from starlette.responses import Response
from typing_extensions import Annotated

from core.methods import get_connection, resource_path
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
def upload_doping_athlete(
    path: Annotated[str, Body(embed=True)],
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

    shutil.copy(path, resource_path("resources/doping-athletes.xlsx"))

    return Response()


@router.put('/orders/upload')
def upload_order(
    path: Annotated[str, Body(embed=True)],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute("UPDATE databases SET date = ? WHERE slug = ?", (str(datetime.now().strftime('%d.%m.%Y')), "orders"))
    connection.commit()

    destination_path = resource_path('resources/order.docx')
    shutil.copy(path, destination_path)

    return Response()


@router.put('/doping-athletes/download')
def download_doping_athlete(
    path: Annotated[str, Body(embed=True)],
):
    shutil.copy(resource_path("resources/doping-athletes.xlsx"), path)
    return Response(status_code=200)


@router.put('/orders/download')
def download_order(
    path: Annotated[str, Body(embed=True)],
):
    shutil.copy(resource_path("resources/order.docx"), path)
    return Response()
