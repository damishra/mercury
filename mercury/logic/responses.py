from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID, uuid4

CREATERESPONSE = """--begin-sql
INSERT INTO response VALUES ($1::uuid, $2::uuid, $3::uuid, $4::jsonb)
--end-sql"""

GETRESPONSES = """--begin-sql
SELECT question.index, question.question, survey.title, survey.id as `sid`, public.user.username, public.user.id as `uid`, response.content, response.id FROM response
JOIN question ON question.id = response.question_id JOIN survey ON question.survey_id = survey.id
JOIN public.user ON public.user.id = response.user_id
WHERE survey.id = $1::uuid
GROUP BY survey.id, question.id, response.id, public.user.id
--end-sql"""


async def create_response(uid: str, qid: str, content):
    try:
        id = uuid4()
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(CREATERESPONSE)
        await statement.fetchrow(id, UUID(uid), UUID(qid), content)
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")
