from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID, uuid4
from mercury.helpers.path import BASEURL


GETSURVEYS = """--begin-sql
SELECT DISTINCT survey.id, survey.title, public.user.id as user_id, public.user.username, COUNT(question.id) as questions 
FROM survey JOIN public.user ON survey.creator_id = public.user.id 
FULL JOIN question ON question.survey_id = survey.id 
GROUP BY survey.id, public.user.id
--end-sql"""

GETSURVEY = """--begin-sql
SELECT survey.id, survey.title, survey.creator_id, public.user.username, question.id as q_id, question.question, question.type, question.options, question.index 
FROM survey JOIN public.user ON survey.creator_id = public.user.id 
FULL JOIN question ON question.survey_id = survey.id 
WHERE survey.id = $1::uuid
GROUP BY survey.id, question.id, public.user.id
--end-sql"""

CREATESURVEY = """--begin-sql
INSERT INTO survey VALUES ($1::uuid, $2::varchar, $3::uuid)
--end-sql"""

UPDATESURVEY = """--begin-sql
UPDATE survey SET title = $1::varchar WHERE id = $2::uuid
--end-sql"""

DELETESURVEY = """--begin-sql
DELETE FROM survey WHERE id = $1::uuid AND creator_id = $2::uuid
--end-sql"""


async def get_all_surveys():
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(GETSURVEYS)
        results = await statement.fetch()
        surveys = []
        for result in results:
            survey = {
                "id": str(result['id']),
                "title": result['title'],
                "questions": result['questions'],
                "url": f"{BASEURL}/surveys/{result['id']}",
                "creator": {
                    "id": str(result['user_id']),
                    "username": result['username'],
                    "url": f"{BASEURL}/users/{result['user_id']}"
                }
            }
            surveys.append(survey)
        return surveys
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def get_one_survey(sid: str):
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(GETSURVEY)
        result = await statement.fetch(UUID(sid))
        survey = {
            "id": str(result[0]['id']),
            "title": result[0]['title'],
            "author": result[0]['username'],
            "author_url": f"{BASEURL}/surveys/{result[0]['creator_id']}",
            "questions": []
        }

        for question in result:
            survey["questions"].append({
                "index": question['index'],
                "id": str(question['q_id']),
                "question": question['question'],
                "type": question['type'],
                "options": question['options'],
            }) if question['q_id'] is not None else ""

        return survey
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def create_survey(title: str, author: str):
    try:
        id = uuid4()
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(CREATESURVEY)
        await statement.fetchrow(id, title, UUID(author))
        return str(id)
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def delete_survey(sid: str, cid: str):
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(DELETESURVEY)
        await statement.fetchrow(UUID(sid), UUID(cid))
        return sid
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")
