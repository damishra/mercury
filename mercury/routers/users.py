from fastapi import APIRouter
from fastapi.responses import JSONResponse
from mercury.logic.users import get_user, get_users


router = APIRouter(prefix="/users")


@router.get('/users')
async def fetch_users():
    users = await get_users()
    JSONResponse(content=users, status_code=200)


@router.get('/users/{user_id}')
async def fetch_user(user_id: str):
    user = await get_user(user_id)
    JSONResponse(content=user, status_code=200)
