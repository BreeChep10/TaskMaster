#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class Project(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS PROJECT
    """

    __tablename__ = "projects"

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    user_id = Column(String(60), ForeignKey('users.id'))
    comments = relationship("ProjectComment",
                            backref="project",
                            cascade="all, delete-orphan")
    tasks = relationship("Task",
                         backref="project",
                         cascade="all, delete-orphan")
