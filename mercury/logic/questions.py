from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID, uuid4


GETAUTHID = """--begin-sql
SELECT public.user.id FROM survey JOIN public.user ON survey.creator_id = public.user.id WHERE survey.id = $1::uuid GROUP BY public.user.id
--end-sql"""

CREATEQUESTION = """--begin-sql
INSERT INTO question VALUES ($1:uuid, $2::text, $3::varchar, $4::jsonb, $5::uuid, $6::int)
--end-sql"""

UPDATEQUESTION = """--begin-sql
UPDATE question SET question.question = $1::text, question.type = $2::varchar, question.index = $3::int, question.options = $4::jsonb WHERE question.id = $5::uuid
--end-sql"""

DELETEQUESTION = """--begin-sql
DELETE FROM survey WHERE survey.id = $1::uuid
--end-sql"""


async def create_question(question: str, type: str, options: list[str], index: int, survey: str):
    try:
        id = uuid4()
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(CREATEQUESTION)
        await statement.fetchrow(id, question, type, index, options, UUID(survey))
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def update_question(question: str, type: str, options: list[str], index: int, id: str):
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(UPDATEQUESTION)
        await statement.fetchrow(question, type, index, options, UUID(id))
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def delete_question(qid: str):
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(DELETEQUESTION)
        await statement.fetchrow(UUID(qid))
        return qid
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")
