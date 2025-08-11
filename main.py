from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# @app.get('/')
# def index():
#   return {'data': {"Profession": "Python Developer" , "status":200, "message":"Response is OK"}}

# @app.get('/about')
# def about():
#   return {"data": {"name":"Faraaz", "status":200 , "message":"Response is Ok..."}}


# @app.get('/blog/unpublished')
# def unpublished():      #! This route must be before the dynamic route 
#   return {'data': 'all the unpublished blog'}


# @app.get('/blog/{id}')
# def show(id:int):         #! id must be in [explicitly defined]....
#   # fetch blog with id=id
#   return {"data": id}

# @app.get('/blog/{id}/comment')
#   # fetch comment of blog with id=id
# def comments(id:int):   #! id must be in [explicitly defined]....
#   return {'data': {'1', '2', '3'}}

# @app.get('/blog')
# def index(limit, published:bool):
#   if published:
#     return {'data': f"{limit} published blogs from the database", "sucess": 200}
#   else:
#     return {'data': f"{limit} blogs from the database", "sucess": 200}
  
 #! Here we have set the default value of parameter 
@app.get('/blog')
def index(limit=10, published:bool= True, sort:Optional[str]= None):  
  if published:
    return {'data': f"{limit} published blogs from the database", "sucess": 200}
  else:
    return {'data': f"{limit} blogs from the database", "sucess": 200}

class Blog(BaseModel):
  title: str
  body : str
  published: Optional[bool] = True


#! for Debuggig: cntrl + Shift + P
@app.post('/blog')
def create_blog(request: Blog):
  if request.published:
    return {'data': f"Blog is create as : {request.title}"}
  else:
    return {'data': f"Blog is cretaed as: {request.title} but it is not published...."}