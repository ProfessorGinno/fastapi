from pydantic import BaseModel
from typing import Union

class Movie(BaseModel):
    id: Union[str, None]
    name: str
    genres: list[str]
    url: str