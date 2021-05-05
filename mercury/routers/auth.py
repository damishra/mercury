from mercury.types.user import User
from typing import Union
from fastapi.responses import JSONResponse
from mercury.logic.auth import register, login, update, delete
from fastapi import APIRouter


router = APIRouter(prefix="/auth")


@router.post("/login", tags=["login"])
async def user_login(user: User):
    token: Union[str, None]
    response: JSONResponse
    token = await login(user.username, user.password)
    if token is not None:
        response = JSONResponse(
            content={'message': 'logged in successfully'}, status_code=200)
        response.set_cookie(
            key="token", value=f"{token}", httponly=True, max_age=21600)
    else:
        response = JSONResponse(
            content={'message': 'login failed'}, status_code=400)
    return response


@router.post("/register", tags=["register"])
async def user_register(user: User):
    generated_id = await register(user.username, user.password, user.email)
    return JSONResponse(content={'id': generated_id}, status_code=201)


@router.put("/update/{user_id}", tags=["update"])
async def user_update(user_id: str, user: User):
    generated_id = await update(user_id, user.username, user.password, user.email)
    return JSONResponse(content={'id': generated_id}, status_code=202)


@router.delete("/delete/{user_id}", tags=["delete"])
async def user_delete(user_id: str):
    generated_id = await delete(user_id)
    return JSONResponse(content={'id': generated_id}, status_code=202)
