from pydantic import BaseModel
from typing import List, Optional


class Question(BaseModel):
    id: Optional[str] = None
    question: Optional[str] = None
    type: Optional[str] = None
    options: Optional[List[str]] = None
    survey: Optional[str] = None
    index: Optional[int] = None
