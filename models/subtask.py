#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from models.enumerations import TaskStatus

class Subtask(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS SUBTASK
    """
    __tablename__ = "subtasks"

    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    task_id = Column(String(60), ForeignKey('tasks.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    subtaskstatus = Column(SqlEnum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    comments = relationship("Comment", backref="subtask")
    #timers = relationship("Timer", backref="subtask")
    #subtaskpriority = relationship("Taskpriority", backref="subtask")
    #taskprogress = relationship("Taskprogress", backref="subtask")
    #taskdependency = relationship("Taskdependency", backref="subtask")
    #taskassignee = relationship("Taskassignee", backref="subtask")
    #taskprogress = relationship("Taskprogress", backref="subtask")
    #taskdependency = relationship("Taskdependency", backref="subtask")
    #taskassignee = relationship("Taskassignee", back