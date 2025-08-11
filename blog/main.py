from fastapi import FastAPI ,Depends , status , Response , HTTPException
from . import schemas , models
from typing import List  
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext





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
  blog = db.query(models.Blog).filter(models.Blog.id ==id)
  if not blog.first():
    return {"status":404, "message": f"No Blog found of id {id}"}
  blog.delete(synchronize_session=False)
  db.commit()
  return {"message": f"blog with id {id} is deleted successfully..."}


@app.put("/blog/{id}")
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return {"message": f"No blog of id:{id} found", "status": 404}
    
    update_data = request.dict(exclude_unset=True)  # only fields sent in request
    for key, value in update_data.items():
        setattr(blog, key, value)
    
    db.commit()
    return {"message": "Updated Successfully"}



@app.get('/blog' ,response_model=List[schemas.ShowBlog] )
def all(db : Session= Depends(get_db)):
  blogs = db.query(models.Blog).all();  
  return blogs 



@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog of id {id} is not found"
        )
    return blog




#! password hashing
pwd_cxt = CryptContext(schemes=["bcrypt"] , deprecated="auto")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user')
def create_user(request: schemas.User , db : Session = Depends(get_db)):
  hassedPassword = pwd_cxt.hash(request.password)
  new_User = models.User(name = request.name, 
                         email = request.email,
                         password = hassedPassword)
  
  db.add(new_User)
  db.commit()
  db.refresh(new_User)
  return new_User
   

  # if request.published:
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments are now published"}
  # else :
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments, but it is not published yet"}
  

# @app.post("/myblog")
# def create_blog(title:str, body:str, totaLikes:int, totalComments:int, published:bool):
#   return {"title":title, "body": body , "totaLikes":totaLikes ,"totalComments": totalComments, "published_at":published}


