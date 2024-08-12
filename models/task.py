#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from models.enumerations import TaskStatus


class Task(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS TASK
    """
    __tablename__ = "tasks"
        
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(String(60), ForeignKey('projects.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    taskstatus = Column(SqlEnum(TaskStatus), default=TaskStatus.NEW, nullable=False)
    comments = relationship("Comment", backref="task")
    subtasks = relationship("Subtask", backref="task")
    #timers = relationship("Timer", backref="task")
    #taskstatus = relationship("Taskstatus", backref="task")
    #taskpriority = relationship("Taskpriority", backref="task")
    #taskprogress = relationship("Taskprogress", backref="task")
    #taskdependency = relationship("Taskdependency", backref="task")