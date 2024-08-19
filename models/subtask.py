#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy import Integer, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.orm import relationship
from models.enumerations import TaskStatus, TaskPriority
from models.timer import Timer


class Subtask(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS SUBTASK
    """
    __tablename__ = "subtasks"

    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    task_id = Column(String(60), ForeignKey('tasks.id'))
    subtaskstatus = Column(SqlEnum(TaskStatus),
                           default=TaskStatus.NEW, nullable=False)
    subtaskpriority = Column(SqlEnum(TaskPriority),
                             default=TaskPriority.MEDIUM, nullable=False)
    timers = relationship("SubtaskTimer", backref="subtask",
                          cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'Subtask',  # Identity for Subtask
    }
