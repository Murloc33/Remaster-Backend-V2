from fastapi import APIRouter

from modules.athletes.general.routers import main_athletes_router
from modules.databases.api import router as databases_router
from modules.documents.general.routers import main_documents_router
from modules.doping_athletes.api import router as doping_athletes
from modules.sports.api import router as spots_router

main_router = APIRouter()

main_router.include_router(main_documents_router)
main_router.include_router(main_athletes_router)
main_router.include_router(doping_athletes)
main_router.include_router(databases_router)
main_router.include_router(spots_router)
