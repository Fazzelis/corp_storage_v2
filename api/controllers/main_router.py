from fastapi.routing import APIRouter
from api.controllers.auth_controller import router as auth_router

main_router = APIRouter()
main_router.include_router(auth_router)
