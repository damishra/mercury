from mercury.logic.auth import check_token
from typing import Optional

from fastapi.params import Cookie
from mercury.types.survey import Survey
from mercury.logic.surveys import create_survey, delete_survey, get_all_surveys, get_one_survey
from fastapi.responses import JSONResponse
from fastapi import APIRouter
