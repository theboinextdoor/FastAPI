from fastapi import FastAPI ,Depends , status , Response , HTTPException
from . import schemas , models, hashing
from typing import List  
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash




app = FastAPI()




models.Base.metadata.create_all(engine)


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

    
@app.post('/blog' , status_code=status.HTTP_201_CREATED , tags=["blogs"])
def create(request: schemas.Blog, db: Session= Depends(get_db)):
  new_blog = models.Blog(title = request.title,
                         body = request.body,
                         user_id = 1
                         )
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return {new_blog}



@app.delete('/blog/{id}', status_code=204, tags=["blogs"])
def destroy(id:int , db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
  if not blog:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} doesn't exist")
  blog.delete(synchronize_session=False)
  db.commit()
  return {"message": f"blog with id {id} is deleted successfully..."}


@app.put("/blog/{id}", tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return {"message": f"No blog of id:{id} found", "status": 404}
    
    update_data = request.dict(exclude_unset=True)  # only fields sent in request
    for key, value in update_data.items():
        setattr(blog, key, value)
    
    db.commit()
    return {"message": "Updated Successfully"}



@app.get('/blog' ,response_model=List[schemas.ShowBlog], tags=["blogs"] )
def all(db : Session= Depends(get_db)):
  blogs = db.query(models.Blog).all();  
  return blogs 



@app.get('/blog/{id}', response_model=schemas.ShowBlog, tags=["blogs"])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog of id {id} is not found"
        )
    return blog




#! password hashing
@app.post('/user', tags=["user"])
def create_user(request: schemas.User , db : Session = Depends(get_db)):
  new_User = models.User(name = request.name, 
                         email = request.email,
                         password = Hash.bcrypt(request.password))
  
  db.add(new_User)
  db.commit()
  db.refresh(new_User)
  return new_User


@app.get('/user/{id}', status_code=200, response_model=schemas.ShowUser, tags=["user"])
def get_user(id : int , db: Session= Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  if not user:
    raise HTTPException(
            status_code=404,
            detail=f"User {id} not found"
        ) 
  return user


@app.get("/allUser" , status_code=200, response_model=List[schemas.ShowUser], tags=["user"])
def show_all_user(db:Session = Depends(get_db)):
  all_users = db.query(models.User).all()
  return all_users

@app.delete("/user/{id}", tags=["user"])
def del_user(id: int, db: Session = Depends(get_db)):
  current_user = db.query(models.User).filter(models.User.id == id).first()
  if not current_user:
    raise HTTPException(status_code=404, detail=f"User with id {id} doesn't exist")
  db.delete(current_user)
  db.commit()
  return {"User Deleted..."}
   
     








































  # if request.published:
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments are now published"}
  # else :
  #   return {f"Blog:{request.title} has {request.likes} likes and total {request.Totalcomments} comments, but it is not published yet"}
  

# @app.post("/myblog")
# def create_blog(title:str, body:str, totaLikes:int, totalComments:int, published:bool):
#   return {"title":title, "body": body , "totaLikes":totaLikes ,"totalComments": totalComments, "published_at":published}


