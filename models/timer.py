#!/usr/bin/python3
from datetime import datetime, timedelta
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from models.base_model import Base, BaseModel
import models


class Timer(BaseModel, Base):
    """
    Timer class to manage task timing.
    """

    __tablename__ = 'timers'

    task_id = Column(String(60), ForeignKey('tasks.id'), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=True)
    

    @property
    def duration(self):
        """
        Calculates and returns the duration as a string in the format 'X days, Y hours'.
        If end_time is not set, returns 'End time not set'.
        """
        if not self.end_time:
            return "End time not set"
        
        # Calculate the difference between the end time and start time
        remaining_time = self.end_time - self.start_time
        
        # Convert the difference into days and from datetime import datetime, timedelta
        days = remaining_time.days
        hours = remaining_time.seconds // 3600
        
        return f"{days} days, {hours} hours"

    def set_end_time(self, end_time):
        """
        Sets the end time for the timer.
        """
        self.end_time = end_time

    def start(self):
        """
        Starts the timer by setting the start_time to the current time.
        """
        self.start_time = datetime.now()

    def stop(self):
        """
        Stops the timer by setting the end_time to the current time.
        """
        self.end_time = datetime.now()


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
