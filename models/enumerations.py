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