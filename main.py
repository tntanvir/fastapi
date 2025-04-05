from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
# uvicorn blogs.main:apps --reload


app=FastAPI()


@app.get('/')
def index():
    return {'data':{'name':'Tanvir'}}

@app.get('/blog')
def blog(limite: int =10 ,publised : bool =True,sort: Optional[str]=None):
    if publised:

        return {'data': f'{limite} {sort}  publised blog fetching'}
    else:
        return {'data': f'{limite} {sort} all blog fetching'}



@app.get('/blog/unpublicd')
def unpublicd():
    return {'data': 'unpublicd'}

@app.get('/blog/{id}')
def singleblog(id:int):
    return {'data': id}



@app.get('/blog/{id}/comment')
def singleblog(id:int):
    return {"id":id,'data': {"nice","good"}}

@app.get('/about')
def about():
    return {'data':'about pagef'}


class BlogModel(BaseModel):
    title : str
    body: str
    publised: Optional[bool]


@app.post('/blog')
def create_blog(request : BlogModel):
    return {'data': f"Blog is created with title : {request.title}"}