#!/usr/bin/python3
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SqlEnum, DateTime
from sqlalchemy.orm import relationship
from models.enumerations import TaskStatus
from datetime import datetime


class Timer(BaseModel, Base):
    """
    CONSTRUCTS THE CLASS TIMER
    """
    __tablename__ = "timers"

    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    