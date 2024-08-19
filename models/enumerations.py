#!/usr/bin/python3
"""
Holds enumerarions for the database
"""
import enum


class TaskStatus(enum.Enum):
    """
    Enumerates the status of a task
    """
    NEW = 1
    IN_PROGRESS = 2
    ON_HOLD = 3
    COMPLETED = 4
    CANCELLED = 5


class TaskPriority(enum.Enum):
    """
    Enumerates the priority of a task
    """
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    IMMEDIATE = 5

class TaskProgress(enum.Enum):
    """
    Enumerates the progress of a task
    """
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    ON_HOLD = 4
    CANCELLED = 5