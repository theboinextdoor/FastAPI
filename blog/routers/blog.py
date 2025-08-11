from fastapi import APIRouter, Depends, status ,HTTPException
from sqlalchemy.orm import Session
from .. import schemas , models , database
from typing import List
from ..repository import blogRepo

router = APIRouter(tags=['blogs'],prefix="/blog")
get_db = database.get_db

@router.post('/' , status_code=status.HTTP_201_CREATED )
def create(request:schemas.Blog, db:Session=Depends(get_db)):
  return blogRepo.create(request,db)


@router.delete('/{id}', status_code=204)
def destroy(id:int , db:Session = Depends(get_db)):
  return blogRepo.destroy(id,db)

@router.put("/{id}")
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
   return blogRepo.update(id, request,db)

@router.get('/' ,response_model=List[schemas.ShowBlog] )
def all(db : Session= Depends(get_db)):
  return blogRepo.getall(db)

@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    return blogRepo.blog_by_id(id, db)

