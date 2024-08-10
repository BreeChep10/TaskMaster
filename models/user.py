#!/usr/bin/env python
"""
User class
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
	__tablename__ = 'users'

	username = Column(String, nullable=False, unique=True)
	email = Column(String, nullable=False, unique=True)
	#tasks = relationship('Task', backref='assignee')
	#comments = relationship('Comment', backref='author')
