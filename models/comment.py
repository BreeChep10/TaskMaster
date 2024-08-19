#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

class TaskComment(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS   TASK COMMENT
    """
    __tablename__ = "task_comments"

    text = Column(Text, nullable=False)
    task_id = Column(String(60), ForeignKey('tasks.id'))
    user_id = Column(String(60), ForeignKey('users.id'))


class ProjectComment(BaseModel, Base):
    """
    Comment for the project
    """
    __tablename__ = "project_comments"

    text = Column(Text, nullable=False)
    project_id = Column(String(60), ForeignKey("projects.id"))
    user_id = Column(String(60), ForeignKey("users.id"))