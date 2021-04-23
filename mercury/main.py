from fastapi import FastAPI
from mercury.routers import auth

app = FastAPI()

app.include_router(auth.router, tags=['auth'])
