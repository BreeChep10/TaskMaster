#!/usr/bin/python3
"""
Database set up
"""
from models.engine.db_storage import DBStorage
from models.user import User
from models.project import Project
from models.task import Task
from models.comment import TaskComment, ProjectComment
from models.subtask import Subtask
from models.timer import Timer, SubtaskTimer
from models.base_model import BaseModel

storage = DBStorage()
storage.reload()