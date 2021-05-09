from fastapi.params import Cookie
from mercury.types.user import User
from typing import Optional, Union
from fastapi.responses import JSONResponse
from mercury.logic.auth import register, login, update, delete, check_token
from fastapi import APIRouter


router = APIRouter(prefix="/auth")


@router.post("/login")
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


@router.post("/register")
async def user_register(user: User):
    generated_id = await register(user.username, user.password, user.email)
    return JSONResponse(content={'id': generated_id}, status_code=201)


@router.put("/update")
async def user_update(user: User, token: Optional[str] = Cookie(None)):
    generated_id = await update(await check_token(token), user.username, user.password, user.email)
    return JSONResponse(content={'id': generated_id}, status_code=202)


@router.delete("/delete")
async def user_delete(token: Optional[str] = Cookie(None)):
    generated_id = await delete(await check_token(token))
    return JSONResponse(content={'id': generated_id}, status_code=202)
