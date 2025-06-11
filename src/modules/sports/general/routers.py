from fastapi import APIRouter

from modules.sports.modules.sports.api import router as sports_router
from modules.sports.modules.sports_programming.api import router as sports_programming_router

main_athletes_router = APIRouter(prefix='/sports')

main_athletes_router.include_router(sports_router)
main_athletes_router.include_router(sports_programming_router)
