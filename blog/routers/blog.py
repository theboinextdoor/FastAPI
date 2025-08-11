from fastapi import APIRouter, Depends, status ,HTTPException
from sqlalchemy.orm import Session
from .. import schemas , models , database
from typing import List

router = APIRouter()
get_db = database.get_db

@router.post('/blog' , status_code=status.HTTP_201_CREATED , tags=["blogs"])
def create(request: schemas.Blog, db: Session= Depends(get_db)):
  new_blog = models.Blog(title = request.title,
                         body = request.body,
                         user_id = 1
                         )
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)
  return {new_blog}


@router.delete('/blog/{id}', status_code=204, tags=["blogs"])
def destroy(id:int , db:Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
  if not blog:
    raise HTTPException(status_code=404, detail=f"Blog with id {id} doesn't exist")
  blog.delete(synchronize_session=False)
  db.commit()
  return {"message": f"blog with id {id} is deleted successfully..."}

@router.put("/blog/{id}", tags=["blogs"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return {"message": f"No blog of id:{id} found", "status": 404}
    
    update_data = request.dict(exclude_unset=True)  # only fields sent in request
    for key, value in update_data.items():
        setattr(blog, key, value)
    
    db.commit()
    return {"message": "Updated Successfully"}

@router.get('/blog' ,response_model=List[schemas.ShowBlog], tags=["blogs"] )
def all(db : Session= Depends(get_db)):
  blogs = db.query(models.Blog).all();  
  return blogs 



@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=["blogs"])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail=f"Blog of id {id} is not found"
        )
    return blog

