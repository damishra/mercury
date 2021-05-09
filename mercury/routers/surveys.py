from mercury.logic.auth import check_token
from typing import Optional

from fastapi.params import Cookie
from mercury.types.survey import Survey
from mercury.logic.surveys import create_survey, delete_survey, get_all_surveys, get_one_survey
from fastapi.responses import JSONResponse
from fastapi import APIRouter


router = APIRouter(prefix='/surveys')


@router.get('/')
async def get_all():
    surveys = await get_all_surveys()
    return JSONResponse(content=surveys, status_code=200)


@router.get('/{survey_id}')
async def get_one(survey_id: str):
    survey = await get_one_survey(survey_id)
    return JSONResponse(content=survey, status_code=200)


@router.post('/')
async def create(survey: Survey, token: Optional[str] = Cookie(None)):
    id = await create_survey(survey.title, await check_token(token))
    return JSONResponse(content={"id": id}, status_code=201)


@router.delete('/{survey_id}')
async def delete(survey_id: str, token: Optional[str] = Cookie(None)):
    id = await delete_survey(survey_id, await check_token(token))
    return JSONResponse(content={"id": id}, status_code=202)
