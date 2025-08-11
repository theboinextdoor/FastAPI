from fastapi import FastAPI
from . import models
from typing import List  
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog , user



app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)



     








































  # if request.published:
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments are now published"}
  # else :
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments, but it is not published yet"}
  

# @app.post("/myblog")
# def create_blog(title:str, body:str, totaLikes:int, totalComments:int, published:bool):
#   return {"title":title, "body": body , "totaLikes":totaLikes ,"totalComments": totalComments, "published_at":published}


