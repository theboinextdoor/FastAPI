from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
  title: str
  body : str
  likes : int
  totalComments : int
  # published: Optional[bool]= False
