from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: Optional[Any] = Field(alias="_id", default=None)
    message : str
    user_to: str
    user_from : str
    delivered: bool = False
    timestamp: datetime = Field(default_factory= datetime.now)

    class Config:
            populate_by_name = True
