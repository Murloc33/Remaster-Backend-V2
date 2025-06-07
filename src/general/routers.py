from fastapi import APIRouter

from modules.athletes.api import router as athletes_router
from modules.documents.api import router as documents_router
from modules.doping_athletes.api import router as doping_router
from modules.databases.api import router as databases_router

main_router = APIRouter()

main_router.include_router(athletes_router)
main_router.include_router(documents_router)
main_router.include_router(doping_router)
main_router.include_router(databases_router)
