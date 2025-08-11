from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
  title: str
  body : str
  likes : int
  Totalcomments : int
  published: Optional[bool]= False
