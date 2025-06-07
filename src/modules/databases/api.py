from datetime import datetime
from sqlite3 import Connection

from fastapi import APIRouter, Depends
from openpyxl import load_workbook
from starlette.responses import Response

from modules.athletes.schemes import Athlete
from core.methods import get_connection
from modules.doping_athletes.schemes import Doping

router = APIRouter(prefix='/databases')


@router.get('/')
def read_database(connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute("Select * from databases")
    result = cursor.fetchall()

    return {"data": result}


@router.put('/doping-athletes/upload')
def update_doping_athlete(doping: Doping, connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute('DELETE FROM doping_athletes')
    cursor.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = ?', ('doping_athletes',))
    connection.commit()

    wb = load_workbook(doping.path)

    for row in wb["Лист1"].iter_rows(min_row=4, values_only=True):
        if not any(row):
            break

        cursor.execute(
            "INSERT INTO  doping_athletes "
            "(full_name, sport, birth_date, violation_description, disqualification_duration, disqualification_start, disqualification_end)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                row[0], row[2],str(row[1]).replace(' 00:00:00', "") , row[3], row[4],
                str(row[5]).replace(' 00:00:00', ""), str(row[6]).replace(' 00:00:00', "")
            )
        )

    cursor.execute('UPDATE databases SET date = ? WHERE slug = ?', (str(datetime.now().strftime('%d.%m.%Y')), "doping-athletes"))
    connection.commit()

    return Response(status_code=200)

@router.put('/order/upload')
def update_order(order: Order, connection: Connection = Depends(get_connection)):
    cursor = connection.cursor()

    cursor.execute("UPDATE databases SET date = ? WHERE slug = ?", (str(datetime.now().strftime('%d.%m.%Y')), "order"))


    destination_path = "../resources/Шаблон_приказа.docx"
    shutil.copy(order.path, destination_path)

    return Response(status_code=200)
