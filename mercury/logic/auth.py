from mercury.helpers.database import DBURI
from typing import Union
from asyncpg import Connection
import asyncpg
from jwt import encode
from os import environ
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID, uuid4
from datetime import datetime
from argon2 import PasswordHasher, Type


HASHER = PasswordHasher(type=Type.ID, hash_len=32,
                        memory_cost=4096, time_cost=3, parallelism=1)


INSERTQ = """--begin-sql
INSERT INTO public.user VALUES ($1::uuid, $2::varchar, $3::varchar, $4::varchar)
--end-sql"""
UPDATEQ = """--begin-sql
UPDATE public.user SET username = $2::varchar, password = $3::varchar, email = $4::varchar WHERE id = $1::uuid
--end-sql"""
PASSWDQ = """--begin-sql
SELECT id, password FROM public.user WHERE username = $1::varchar
--end-sql"""
SELECTQ = """--begin-sql
SELECT username, password, email FROM public.user WHERE id = $1::uuid
--end-sql"""
DELETEQ = """--begin-sql
DELETE FROM public.user WHERE id = $1::uuid
--end-sql"""


async def register(username: str, password: str, email: str) -> str:
    try:
        id = uuid4()
        hashed_password = HASHER.hash(password)
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(INSERTQ)
        await statement.fetchval(id, username, hashed_password, email)
        await connection.close()
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def login(username: str, password: str) -> Union[str, None]:
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(PASSWDQ)
        result = await statement.fetchrow(username)
        await connection.close()
        id = result["id"]
        hashed_password: str = result["password"]
        if HASHER.verify(hashed_password, password):
            return encode(
                {"id": str(id), "exp": int(
                    datetime.utcnow().timestamp()) + 21600},
                environ.get("JWTKEY"), algorithm="HS256")
    except Exception:
        raise HTTPException(status_code=401, detail="unauthorized")


async def update(uid: str, username: str, password: str, email: str) -> str:
    id = UUID(hex=uid)
    hashed_password = HASHER.hash(password)
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(SELECTQ)
        result = await statement.fetchrow(uid)
        if username == None or username == result['username']:
            username = result['username']
        try:
            if password == None or HASHER.verify(result['password'], password):
                password = result['password']
        except Exception:
            pass
        if email == None or email == result['email']:
            email = result['email']
        statement: PreparedStatement = await connection.prepare(UPDATEQ)
        await statement.fetchrow(id, username, hashed_password, email)
        await connection.close()
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def delete(uid: str) -> str:
    try:
        id = UUID(hex=uid)
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(DELETEQ)
        await statement.fetchrow(id)
        await connection.close()
        return str(id)
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
