from fastapi import FastAPI
from mercury.routers import auth, users


app = FastAPI()

app.include_router(auth.router, tags=['auth'])
app.include_router(users.router, tags=['users'])
