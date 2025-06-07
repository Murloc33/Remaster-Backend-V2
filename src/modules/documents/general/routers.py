from fastapi import APIRouter

from modules.documents.modules.athletes.api import router as athletes_router
from modules.documents.modules.document.api import router as document_router
from modules.documents.modules.documents.api import router as documents_router
from modules.documents.modules.orders.api import router as orders_router

main_documents_router = APIRouter(prefix='/documents')

main_documents_router.include_router(documents_router)
main_documents_router.include_router(document_router)
main_documents_router.include_router(athletes_router)
main_documents_router.include_router(orders_router)
