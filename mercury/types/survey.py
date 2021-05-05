from pydantic import BaseModel
from typing import Optional


class Survey(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
