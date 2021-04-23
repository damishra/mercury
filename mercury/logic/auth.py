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


HASHER = PasswordHasher(type=Type.ID)


INSERTQ = "INSERT INTO auth VALUES ($1::uuid, $2::varchar, $3::bytea, $4::varchar, $5::bigint, $6::bigint)"
UPDATEQ = "UPDATE auth SET username = $2::varchar, password = $3::bytea, email = $4::varchar, updated = $5::bigint WHERE id = $1::uuid"
PASSWDQ = "SELECT id, password FROM auth WHERE username = $1::varchar"
SELECTQ = "SELECT username, password, email FROM auth WHERE id = $1::uuid"
DELETEQ = "DELETE FROM auth WHERE id = $1::uuid"


async def register(username: str, password: str, email: str) -> str:
    try:
        id = uuid4()
        hashed_password = HASHER.hash(password.encode('UTF-8'))
        created = int(datetime.utcnow().timestamp())
        updated = int(datetime.utcnow().timestamp())
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(INSERTQ)
        await statement.fetchval(id, username, hashed_password.encode('UTF-8'), email, created, updated)
        await connection.close()
        return id.hex
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
        hashed_password = result["password"]
        if HASHER.verify(hashed_password, password.encode("UTF-8")):
            return encode(
                {"id": id.hex, "exp": int(
                    datetime.utcnow().timestamp()) + 21600},
                environ.get("JWTKEY"), algorithm="HS256")
    except Exception:
        raise HTTPException(status_code=401, detail="unauthorized")


async def update(uid: str, username: str, password: str, email: str) -> str:
    id = UUID(hex=uid)
    hashed_password = HASHER.hash(password.encode('UTF-8'))
    updated = int(datetime.utcnow().timestamp())
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(SELECTQ)
        result = await statement.fetchrow(uid)
        if username == None or username == result['username']:
            username = result['username']
        if password == None or HASHER.verify(result['password'], password.encode('utf-8')):
            password = result['password']
        if email == None or email == result['email']:
            email = result['email']
        statement: PreparedStatement = await connection.prepare(UPDATEQ)
        await statement.fetchrow(id, username, hashed_password.encode('utf-8'), email, updated)
        await connection.close()
        return id.hex
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
        return id.hex
    except Exception:
        raise HTTPException(status_code=500, detail="internal server error")
