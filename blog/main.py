from fastapi import FastAPI ,Depends , status , Response
from . import schemas , models
from typing import Optional
from .database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()




models.Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

    
@app.post('/blog' , status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session= Depends(get_db)):
  new_blog = models.Blog(title = request.title,
                         body = request.body,
                         likes = request.likes,
                         totalComments = request.totalComments
                         )
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return new_blog

@app.delete('/blog/{id}', status_code=204)
def destroy(id:int , db:Session = Depends(get_db)):
  db.query(models.Blog).filter(models.Blog.id ==id).delete(synchronize_session=False)
  db.commit()
  return {"data": f"blog id: {id} is deleted", "status":200}

@app.get('/blog')
def all(db : Session= Depends(get_db)):
  blogs = db.query(models.Blog).all();  
  return blogs 

@app.get('/blog/{id}' , status_code=200)
def show(id:int, response:Response, db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    # raise HTTPExecption(status_code=404 ,
    #                      details=f"Blog of id {id} is not found"
    #                        )
   response.status_code = status.HTTP_404_NOT_FOUND
   return {"response":  {
     "message" : f"Blog of id {id} is not found",
     "data": "null",
     "status" : 404
   }}
  return blog

  # if request.published:
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments are now published"}
  # else :
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments, but it is not published yet"}
  

# @app.post("/myblog")
# def create_blog(title:str, body:str, totaLikes:int, totalComments:int, published:bool):
#   return {"title":title, "body": body , "totaLikes":totaLikes ,"totalComments": totalComments, "published_at":published}


