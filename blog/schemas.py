from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
  title: Optional[str] = None
  body : Optional[str] = None
  likes : Optional[int] = None
  totalComments : Optional[int] = None


class ShowBlog(Blog):
  title: Optional[str] = None
  body : Optional[str] = None
  # likes : Optional[int] = None
  # totalComments : Optional[int] = None

  class Config():
    orm_mode = True

class User(BaseModel):
  name: str
  email: str
  password: str
  
class ShowUser(BaseModel):
  name: str
  email: str

  class Config():
    orm_mode = True


