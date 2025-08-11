from fastapi import FastAPI
from . import schemas
from typing import Optional


app = FastAPI()


    
@app.post('/blog')
def create(request: schemas.Blog):
  if request.published:
    return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments are now published"}
  else :
    return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments, but it is not published yet"}
  

@app.post("/myblog")
def create_blog(title:str, body:str, totaLikes:int, totalComments:int, published:bool):
  return {"title":title, "body": body , "totaLikes":totaLikes ,"totalComments": totalComments, "published_at":published}


