from fastapi import APIRouter

from api.v1.jobs import JobsRest
from api.v1 import route_login
from api.v1.users import UsersRest

api_router = APIRouter()

api_router.include_router(UsersRest.router, prefix="/users", tags=["users"])
api_router.include_router(JobsRest.router, prefix="/job", tags=["Jobs"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
