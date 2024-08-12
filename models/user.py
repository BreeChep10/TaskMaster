#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS USER
    """
    __tablename__ = "users"
        
    username = Column(String(128), unique=True, nullable=False)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    #projects = relationship("Project", backref="user")
    #tasks = relationship("Task", backref="user")
    #comments = relationship("Comment", backref="user")