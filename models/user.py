#!/usr/bin/python3
"""
User Class from Models
"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS USER
    """
    __tablename__ = "users"

    username = Column(String(128), nullable=False)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    projects = relationship("Project", backref="user",
                            cascade="all, delete-orphan")
    tasks = relationship("Task", backref="user", cascade="all, delete-orphan")
    task_comments = relationship("TaskComment",
                                 backref="user", cascade="all, delete-orphan")
    project_comment = relationship("ProjectComment",
                                   backref="user",
                                   cascade="all, delete-orphan")
