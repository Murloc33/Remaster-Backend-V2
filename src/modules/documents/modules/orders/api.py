from sqlite3 import Connection

from docxtpl import DocxTemplate
from fastapi import Depends, APIRouter, Body, Path
from starlette.responses import Response
from typing_extensions import Annotated

from core.methods import get_connection, resource_path
from modules.documents.modules.orders.methods import get_order

router = APIRouter()


@router.post("/{document_id}/orders")
def create_order(
    document_id: Annotated[int, Path()],
    path: Annotated[str, Body(embed=True)],
    connection: Annotated[Connection, Depends(get_connection)]
):
    cursor = connection.cursor()

    cursor.execute('SELECT id, title FROM municipalities')
    municipalities = {e['id']: e['title'] for e in cursor.fetchall()}

    cursor.execute('SELECT id, title FROM organizations')
    organizations = {e['id']: e['title'] for e in cursor.fetchall()}

    order = get_order(connection, document_id)

    document = DocxTemplate(resource_path("resources/orders.docx"))
    document.render(
        {
            'sports_category_name': order.sports_category_name,
            'sports': [
                {
                    'n': f'{sport_number}.',
                    'm': sport.name,
                    'athletes': (
                        [
                            {
                                'n': f'{sport_number}.{athlete_number}',
                                'name': athlete.full_name,
                                'date': athlete.birth_date,
                                'm': municipalities.get(athlete.municipality_id),
                                'o': organizations.get(athlete.organization_id),
                            } for athlete_number, athlete in enumerate(sport.athletes, start=1)
                        ]
                    )
                } for sport_number, sport in enumerate(order.sports, start=1)
            ]
        }
    )

    document.save(path)

    return Response()
