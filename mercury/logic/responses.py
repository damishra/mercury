from typing import Any, Dict, List
from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID, uuid4

CREATERESPONSE = """--begin-sql
INSERT INTO response VALUES ($1::uuid, $2::uuid, $3::uuid, $4::jsonb)
--end-sql"""


async def create_response(uid: str, qid: str, content: List[Dict[str, Any]]):
    try:
        id = uuid4()
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(CREATERESPONSE)
        await statement.fetchrow(id, UUID(uid), UUID(qid), content)
        await connection.close()
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def fetch_responses(sid: str):
    try:
        id = UUID(sid)
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")
