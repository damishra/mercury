from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID
from mercury.helpers.path import BASEURL

GETUSERS = """--begin-sql
SELECT public.user.id, public.user.username, survey.id as survey_id, survey.title, survey.creator_id
FROM public.user FULL JOIN survey ON public.user.id = survey.creator_id 
GROUP BY public.user.id, survey.id ORDER BY public.user.id ASC
--end-sql"""
GETUSER = """--begin-sql
SELECT public.user.id, public.user.username, survey.id as survey_id, survey.title, survey.creator_id 
FROM public.user FULL JOIN survey ON public.user.id = survey.creator_id  
WHERE public.user.id = $1::uuid 
GROUP BY public.user.id, survey.id
--end-sql"""


async def get_users():
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        results = await connection.fetch(GETUSERS)
        users = []
        surveys = []
        username: str = ""
        for result in results:
            if username != result['username']:
                username = result['username']
                users.append({
                    "id": str(result['id']),
                    "username": result['username'],
                    "avatar": f"https://avatars.dicebear.com/api/avataaars/{str(result['id'])}.svg",
                    "url": f"{BASEURL}/users/{str(result['id'])}",
                    "surveys": [],
                })
            surveys.append({
                "id": str(result['survey_id']),
                "title": result['title'],
                "creator": str(result['creator_id']),
                "url": f"{BASEURL}/surveys/{str(result['survey_id'])}"
            }) if result['survey_id'] is not None else ""

        await connection.close()
        for survey in surveys:
            for i, user in enumerate(users):
                if user['id'] == survey['creator']:
                    break
            else:
                i = -1
            if i != -1:
                users[i]['surveys'].append(survey)
        return users
    except Exception:
        raise HTTPException(
            status_code=500, detail="internal server error")


async def get_user(uid: str):
    try:
        id = UUID(hex=uid)
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        statement: PreparedStatement = await connection.prepare(GETUSER)
        results = await statement.fetch(id)
        user = {
            "id": str(results[0]["id"]),
            "username": results[0]["username"],
            "avatar": f"https://avatars.dicebear.com/api/avataaars/{str(results[0]['id'])}.svg",
            "surveys": [],
        }
        for result in results:
            if result["id"] == result["creator_id"]:
                user["surveys"].append(
                    {
                        "id": str(result['survey_id']),
                        "title": result['title'],
                        "url": f"{BASEURL}/surveys/{result['survey_id']}",
                    }) if result['survey_id'] != None else ""
        await connection.close()
        return user
    except Exception:
        raise HTTPException(
            status_code=404, detail="not found")
