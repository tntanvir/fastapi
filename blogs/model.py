from sqlalchemy import Column, Boolean, Integer, String, Float,ForeignKey
from .database import Base
from sqlalchemy.orm import Relationship


class Blog(Base):
    __tablename__ = "Blog"
    id =Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body =Column(String)
    user_id = Column(Integer, ForeignKey('User.id'))


    creator = Relationship("User", back_populates="blogs")
class User(Base):
    __tablename__ = "User"
    id =Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email =Column(String)
    password =Column(String)

    blogs = Relationship("Blog", back_populates="creator")

