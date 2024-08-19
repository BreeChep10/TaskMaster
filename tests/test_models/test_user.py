#!/usr/bin/python3
"""
Test User class
"""
from datetime import datetime
import inspect
from celery import Task
import models
import pep8 as pycodestyle
import time
import unittest
import uuid
from unittest import mock
from models.comment import ProjectComment, TaskComment
from models.user import User
from models.project import Project
from models.task import Task
module_doc = User.__doc__


class TestUserDocs(unittest.TestCase):
    """
    Tests to check documentation of user class
    """

    @classmethod
    def setUpClass(cls):
        """
        setup func for docstring test
        """
        cls.user_funcs = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_comformance(self):
        """
        Test that models/user.py comforms to pep
        """
        for path in ['models/user.py',
                     'tests/test_models/test_user.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(module_doc, None,
                         "User.py needs a docstring")
        self.assertTrue(len(module_doc) >= 1,
                        "User class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the user class docstring
        """
        self.assertIsNot(User.__doc__, None,
                         "User class needs a doc string")
        self.assertTrue(len(User.__doc__) >= 1,
                        "user class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the usr class funcs docstrings
        """
        for func in self.user_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestUser(unittest.TestCase):
    """
    Test the user class
    """
    @classmethod
    def setUpClass(cls) -> None:
        new_user = User(username="williams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")

        new_project = Project(name="taskmanager",
                              description="Taskmanager project",
                              user_id=new_user.id)
        new_task = Task(name="introduction",
                        project_id=new_project.id,
                        user_id=new_user.id
                        )
        task_comment = TaskComment(text="simple task",
                                   user_id=new_user.id,
                                   task_id=new_task.id)
        project_comment = ProjectComment(text="a simple project",
                                         project_id=new_project.id,
                                         user_id=new_user.id)

        new_user.save()
        new_project.save()
        new_task.save()
        task_comment.save()
        project_comment.save()
        cls.new_user = new_user
        cls.new_project = new_project
        cls.new_task = new_task
        cls.task_comment = task_comment
        cls.project_comment = project_comment
        print("Classes created")

    @classmethod
    def tearDownClass(cls):
        """
        TEARDOWN CLASS
        """
        cls.new_user.delete()
        cls.new_project.delete()
        cls.new_task.delete()
        cls.task_comment.delete()
        cls.project_comment.delete()
        models.storage.save()

    def test_instantiation(self):
        """
        Test the class instanciation
        """
        user = User()
        self.assertIs(type(user), User)
        print("user is user")

    def Test_attributes(self):
        """
        Test  the user's attributes
        """
        self.assertTrue(hasattr(self.new_user, "firstname"))
        self.assertTrue(hasattr(self.new_user, "lastname"))
        self.assertTrue(hasattr(self.new_user, "email"))
        self.assertTrue(hasattr(self.new_user, "username"))
        self.assertTrue(hasattr(self.new_user, "password"))
