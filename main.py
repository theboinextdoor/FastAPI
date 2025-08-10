from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
  return {'data': {"Profession": "Python Developer" , "status":200, "message":"Response is OK"}}

@app.get('/about')
def about():
  return {"data": {"name":"Faraaz", "status":200 , "message":"Response is Ok..."}}