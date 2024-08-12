#!/usr/bin/python3
"""DATABASE STORAGE"""
import models
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from eralchemy import render_er


class DBStorage:
    """
    SQLALCHEMY DATABASE CONNECTION
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        DB STORAGE SET UP
        """
        TASKMANAGER_MYSQL_USER = "taskmanager_dev"
        TASKMANAGER_MYSQL_PWD = "taskmanager_dev_pwd"
        TASKMANAGER_MYSQL_HOST = "localhost"
        TASKMANAGER_MYSQL_DB = "taskmanager_dev_db"
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(TASKMANAGER_MYSQL_USER,
                                             TASKMANAGER_MYSQL_PWD,
                                             TASKMANAGER_MYSQL_HOST,
                                             TASKMANAGER_MYSQL_DB))


        
    def all(self, cls=None):
        """returns a dictionary of the query
        dictionary = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            query = self.__session.query(cls)

            for item in query:
                k = f"{type(item).__name__}.{item.id}"
                dictionary[k] = item
        else:
            all = [User, Recipe, Tag, Comment]
            for i in all:
                query = self.__session.query(i)
                for item in query:
                    k = f"{type(item).__name__}.{item.id}"
                    dictionary[k] = item
        return dictionary"""
        pass

    def new(self, obj):
        """
        ADD A NEW OBJECT TO THE SESSION
        """
        self.__session.add(obj)

    def save(self):
        """
        COMMIT  CHANGES
        """
        self.__session.commit()

    def delete(self, obj):
        """
        DELETES AN OBJECT
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        REFRESHES DATABASE DATA
        """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        scope = scoped_session(factory)
        self.__session = scope

    def close(self):
        """
        DISCONNECTS A SESSION
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        TRIES TO FETCH AN OBJECT
        """
        if cls and id:
            try:
                result = [v for k, v in self.all(cls).
                          items() if k.split(".")[1] == id]
                if result != []:
                    return result[0]
            except Exception:
                pass
        return None

    def count(self, cls=None):
        '''
        COUNTS THE NUMBER OF OBJECTS IN STORGE
        '''
        if cls:
            return len(self.all(cls))
        else:
            return len(self.all())