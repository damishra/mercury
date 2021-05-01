from typing import Any, Dict, List
from mercury.helpers.database import DBURI
from asyncpg import Connection
import asyncpg
from fastapi.exceptions import HTTPException
from asyncpg.prepared_stmt import PreparedStatement
from uuid import UUID

GETUSERS = "SELECT public.user.id, public.user.username, survey.id as survey_id, survey.title FROM public.user FULL JOIN survey ON public.user.id = survey.creator_id GROUP BY public.user.id, survey.id"
GETUSER = "SELECT public.user.id, public.user.username, survey.id as survey_id, survey.title FROM public.user FULL JOIN survey ON public.user.id = survey.creator_id  WHERE public.user.id = $1::uuid GROUP BY public.user.id, survey.id;"


async def get_users() -> List[Dict[str, Any]]:
    try:
        connection: Connection = await asyncpg.connect(dsn=DBURI)
        results = await connection.fetch(GETUSERS)
        users = []
        user = {}
        surveys = []
        username: str = ""
        for result in results:
            if result["username"] != username:
                username = result["username"]
                user = {
                    "id": str(result["id"]),
                    "username": result["username"],
                    "surveys": surveys,
                }
                users.append(user)
                users[len(users)-1]["surveys"].append({"id": result['survey_id'],
                                                       "title": result['title']}) if result['survey_id'] != None else ""

            else:
                users[len(users)-1]["surveys"].append({"id": result['survey_id'],
                                                       "title": result['title']}) if result['survey_id'] != None else ""
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
        user = {"id": str(results[0]["id"]),
                "username": results[0]["username"], "surveys": []}
        for result in results:
            user["surveys"].append(
                {"id": result['survey_id'], "title": result['title']}) if result['survey_id'] != None else ""
        return user
    except Exception:
        raise HTTPException(
            status_code=404, detail="not found")
