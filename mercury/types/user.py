from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
