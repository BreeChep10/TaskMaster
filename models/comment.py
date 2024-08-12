#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

class Comment(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS COMMENT
    """
    __tablename__ = "comments"

    text = Column(Text, nullable=False)
    task_id = Column(String(60), ForeignKey('tasks.id'))
    user_id = Column(String(60), ForeignKey('users.id'))