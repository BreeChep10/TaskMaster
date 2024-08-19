#!/usr/bin/python3
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from models.base_model import Base, BaseModel
import models


class Timer(BaseModel, Base):
    """
    Timer class to track the duration of tasks
    """
    __tablename__ = 'timers'

    task_id = Column(String(60), ForeignKey('tasks.id'), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    @property
    def duration(self):
        """
        Calculate the duration in secs
        """
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def start(self):
        """
        Start the timer by setting the start_time to the current time
        """
        self.start_time = datetime.utcnow()
        models.storage.save()

    def stop(self):
        """
        Stop the timer by setting the end_time to the current time
        """
        self.end_time = datetime.utcnow()
        models.storage.save()

    def reset(self):
        """
        Reset the timer by clearing start_time and end_time
        """
        self.start_time = datetime.utcnow()
        self.end_time = None
        models.storage.save()


class SubtaskTimer(BaseModel, Base):
    """
    Timer class to track the duration of subtasks
    """
    __tablename__ = 'subtask_timers'

    subtask_id = Column(String(60), ForeignKey('subtasks.id'), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    @property
    def duration(self):
        """
        Calculate the duration in seconds
        """
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def start(self):
        """
        Start the timer by setting the start_time to the current time
        """
        self.start_time = datetime.utcnow()
        models.storage.save()

    def stop(self):
        """
        Stop the timer by setting the end_time to the current time
        """
        self.end_time = datetime.utcnow()
        models.storage.save()

    def reset(self):
        """
        Reset the timer by clearing start_time and end_time
        """
        self.start_time = datetime.utcnow()
        self.end_time = None
        models.storage.save()
