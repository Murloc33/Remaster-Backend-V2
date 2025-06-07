from fastapi import APIRouter

from modules.athletes.modules.athlete.api import router as athlete_router

main_athletes_router = APIRouter(prefix='/athletes')

main_athletes_router.include_router(athlete_router)
