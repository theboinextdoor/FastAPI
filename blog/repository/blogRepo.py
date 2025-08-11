from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas



def create(request:schemas.Blog, db:Session):
  new_blog = models.Blog(title = request.title,
                         body = request.body,
                         user_id = 1
                         )
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return {new_blog}

def destroy(id, db:Session ):
  blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
  if not blog:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} doesn't exist")
  blog.delete(synchronize_session=False)
  db.commit()
  return {"message": f"blog with id {id} is deleted successfully..."}

def update(id, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
      return {"message": f"No blog of id:{id} found", "status": 404}
    
    update_data = request.dict(exclude_unset=True)  # only fields sent in request
    for key, value in update_data.items():
        setattr(blog, key, value)
    
    db.commit()
    return {"message": "Updated Successfully"}

def getall(db: Session):
  blogs = db.query(models.Blog).all();  
  return blogs 

def blog_by_id(id ,db:Session ):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog of id {id} is not found"
        )
  return blog