#!/usr/bin/python3
from turtle import back
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from models.enumerations import TaskStatus
from models.enumerations import TaskPriority, TaskProgress
from models.timer import Timer


class Task(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS TASK
    """
    __tablename__ = "tasks"

    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    taskstatus = Column(SqlEnum(TaskStatus),
                        default=TaskStatus.NEW,
                        nullable=False)
    comments = relationship("TaskComment",
                            backref="task",
                            cascade="all, delete-orphan")
    subtasks = relationship("Subtask",
                            backref="task",
                            cascade="all, delete-orphan")
    timers = relationship("Timer",
                          backref="task",
                          cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'Task',  # Identity for Task
    }
    taskpriority = Column(SqlEnum(TaskPriority),
                          default=TaskPriority.MEDIUM,
                          nullable=False)
    taskprogress = Column(SqlEnum(TaskProgress),
                          default=TaskProgress.NOT_STARTED,
                          nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    # taskdependency = relationship("Taskdependency", backref="task")
