from fastapi import APIRouter

from modules.sports.modules.sports.api import router as sports_router
from modules.sports.modules.sports_programming.api import router as sports_programming_router
from modules.sports.modules.computer_sports.api import router as computer_sports_router

main_sports_router = APIRouter(prefix='/sports')

main_sports_router.include_router(sports_router)
main_sports_router.include_router(sports_programming_router)
main_sports_router.include_router(computer_sports_router)

