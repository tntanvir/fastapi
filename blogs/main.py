from fastapi import FastAPI,Depends,status,Response,HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Blog,User,ShowUser,Login
from . import model
from .database import engine,Base,SessionLocal
from sqlalchemy.orm import Session
from .token import create_access_token
from blogs import oauth2


apps= FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@apps.get('/blog',tags=['Blog'])
def allblog(db:Session=Depends(get_db)):
    blogs=db.query(model.Blog).all()
    return blogs

@apps.post('/blog',status_code=status.HTTP_201_CREATED,tags=['Blog'])
def create(request : Blog,db:Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@apps.get('/blog/id',status_code=202,tags=['Blog'])
def show(id,response : Response ,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'massage': f"Blog with the id {id} is not available"}
    return blog

@apps.delete('/blog/id',status_code=202,tags=['Blog'])
def deleteBlog(id,db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return {'massage': f"Blog delete"}
@apps.put('/blog/id',status_code=202,tags=['Blog'])
def updateBlog(id,request : Blog, db:Session=Depends(get_db)):
    blog=db.query(model.Blog).filter(model.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} not found')
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return {'massage': f"Blog with id {id} is updated"}





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@apps.post('/register',response_model=ShowUser,tags=['AUTH'])
def create_user(request:User,db:Session=Depends(get_db)):
    hashpassword = pwd_context.hash(request.password)
    new_user=model.User(name=request.name,email=request.email,password=hashpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @apps.post('/login',tags=['AUTH'])
# def login(request:OAuth2PasswordRequestForm,db:Session=Depends(get_db)):
#     user= db.query(model.User).filter(model.User.email == request.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    

#     varified =pwd_context.verify(request.password, user.password)

#     if not varified:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalide Info')
    
#     access_token = create_access_token(data={'sub': user.email})
#     return {'access_token': access_token, 'token_type': 'bearer'}
@apps.post('/login',tags=['AUTH'])
def login(request: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user= db.query(model.User).filter(model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    

    varified =pwd_context.verify(request.password, user.password)

    if not varified:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Invalide Info')

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

    # return user

    



@apps.get('/user/id',response_model=ShowUser,tags=['USER'])
def user_info(id,db:Session=Depends(get_db)):
    user= db.query(model.User).filter(model.User.id == id).first()
    
    return user
