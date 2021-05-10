from mercury.helpers.path import BASEURL
from fastapi import FastAPI
from starlette.responses import JSONResponse, RedirectResponse
from mercury.routers import auth, users, surveys


app = FastAPI()


@app.get('/')
async def root():
    return RedirectResponse(url="/docs")

app.include_router(auth.router, tags=['auth'])
app.include_router(users.router, tags=['users'])
app.include_router(surveys.router, tags=['surveys'])
