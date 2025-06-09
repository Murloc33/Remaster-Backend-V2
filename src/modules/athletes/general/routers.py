from fastapi import APIRouter

from modules.athletes.modules.athlete.api import router as athlete_router
from modules.athletes.modules.file.api import router as athlete_file_router

main_athletes_router = APIRouter(prefix='/athletes')

main_athletes_router.include_router(athlete_router)
main_athletes_router.include_router(athlete_file_router)
