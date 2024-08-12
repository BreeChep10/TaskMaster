#!/usr/bin/python3
"""
Database set up
"""
from models.engine.db_storage import DBStorage
from models.user import User
from models.project import Project
from models.task import Task
from models.comment import Comment
from models.subtask import Subtask

storage = DBStorage()
storage.reload()