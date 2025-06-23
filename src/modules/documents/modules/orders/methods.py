from datetime import datetime
from sqlite3 import Connection
from typing import Dict, List

from modules.documents.modules.orders.sсhemes import Order, Sport, Athletes

sports_category = {
    1: 'кандидат в мастера спорта',
    2: 'первый спортивный разряд'
}


def get_order(connection: Connection, document_id: int) -> Order:
    cursor = connection.cursor()

    cursor.execute('SELECT sports_category_id FROM documents WHERE id = ?', (document_id,))
    sports_category_name = sports_category[cursor.fetchone()["sports_category_id"]]

    cursor.execute('SELECT * FROM sports')
    sports_data = {value['id']: value['name'] for value in cursor.fetchall()}

    cursor.execute(
        (
            'SELECT * FROM document_athletes '
            'WHERE document_id = ? AND is_sports_category_granted = true AND is_doping_check_passed = true'
        ),
        (document_id,)
    )
    athletes_data = cursor.fetchall()

    sports: Dict[str, List[Athletes]] = {}

    for athlete in athletes_data:
        sport_name = sports_data[athlete['sport_id']]

        if sport_name not in sports.keys():
            sports[sport_name] = []

        sports[sport_name].append(
            Athletes(
                full_name=athlete['full_name'],
                birth_date=datetime.strptime(athlete['birth_date'], "%Y-%m-%d").strftime("%d.%m.%Y"),
                municipality_id=athlete['municipality_id'],
                organization_id=athlete['organization_id']
            )
        )

    return Order(
        sports_category_name=sports_category_name,
        sports=sorted(
            [
                Sport(
                    name=sport_name,
                    athletes=sorted(athletes, key=lambda x: (x.full_name, x.birth_date, x.municipality_id, x.organization_id))
                ) for sport_name, athletes in sports.items()
            ],
            key=lambda x: x.name
        )
    )
