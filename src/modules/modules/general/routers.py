from fastapi import APIRouter

from modules.modules.modules.athletics_place.api import router as athletics_place_router
from modules.modules.modules.computer_sports.api import router as computer_sports_router
from modules.modules.modules.modules.api import router as modules_router
from modules.modules.modules.sports_programming.api import router as sports_programming_router
from modules.modules.modules.athletics_result.api import router as athletics_result_router

main_sports_router = APIRouter(prefix='/modules')

main_sports_router.include_router(modules_router)
main_sports_router.include_router(sports_programming_router)
main_sports_router.include_router(computer_sports_router)
main_sports_router.include_router(athletics_place_router)
main_sports_router.include_router(athletics_result_router)

