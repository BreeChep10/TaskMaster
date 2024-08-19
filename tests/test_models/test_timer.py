#!/usr/bin/python3
"""
Test Timer class
"""
import inspect
import pep8 as pycodestyle
import unittest
from datetime import datetime, timedelta
from models.timer import Timer
from models.task import Task
from models.user import User
from models.project import Project
import models
module_doc = Timer.__doc__


class TestTimerDocs(unittest.TestCase):
    """
    Tests to check documentation of Timer class
    """

    def setUp(self):
        """
        Setup for docstring tests
        """
        self.timer_funcs = inspect.getmembers(Timer, inspect.isfunction)

    def test_pep8_conformance(self):
        """
        Test that models/timer.py conforms to pep8
        """
        for path in ['models/timer.py',
                     'tests/test_models/test_timer.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(module_doc, None,
                         "timer.py needs a docstring")
        self.assertTrue(len(module_doc) >= 1,
                        "Timer class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the Timer class docstring
        """
        self.assertIsNot(Timer.__doc__, None,
                         "Timer class needs a doc string")
        self.assertTrue(len(Timer.__doc__) >= 1,
                        "Timer class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the Timer class functions docstrings
        """
        for func in self.timer_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestTimer(unittest.TestCase):
    """
    Test the Timer class
    """

    def test_instantiation(self):
        """
        Test the class instantiation using Timer
        """
        user = User(username="liams",
                    firstname="will",
                    lastname="kub",
                    email="test_email",
                    password="1234")
        user.save()

        project = Project(name="taskmanager",
                          description="Taskmanager project",
                          user_id=user.id)
        project.save()

        task = Task(name="introduction",
                    project_id=project.id,
                    user_id=user.id)
        task.save()

        timer = Timer(task_id=task.id)
        timer.save()

        self.assertIs(type(timer), Timer)
        timer.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_start_timer(self):
        """
        Test starting the timer
        """
        user = User(username="liams",
                    firstname="will",
                    lastname="kub",
                    email="test_email",
                    password="1234")
        user.save()

        project = Project(name="taskmanager",
                          description="Taskmanager project",
                          user_id=user.id)
        project.save()

        task = Task(name="introduction",
                    project_id=project.id,
                    user_id=user.id)
        task.save()

        timer = Timer(task_id=task.id)
        timer.start()
        timer.save()
        self.assertIsNotNone(timer.start_time)

        timer.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_stop_timer(self):
        """
        Test stopping the timer
        """
        user = User(username="liams",
                    firstname="will",
                    lastname="kub",
                    email="test_email",
                    password="1234")
        user.save()

        project = Project(name="taskmanager",
                          description="Taskmanager project",
                          user_id=user.id)
        project.save()

        task = Task(name="introduction",
                    project_id=project.id,
                    user_id=user.id)
        task.save()

        timer = Timer(task_id=task.id)
        timer.start()
        timer.stop()
        self.assertIsNotNone(timer.end_time)
        timer.save()

        timer.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_duration(self):
        """
        Test calculating the duration
        """
        user = User(username="liams",
                    firstname="will",
                    lastname="kub",
                    email="test_email",
                    password="1234")
        user.save()

        project = Project(name="taskmanager",
                          description="Taskmanager project",
                          user_id=user.id)
        project.save()

        task = Task(name="introduction",
                    project_id=project.id,
                    user_id=user.id)
        task.save()

        timer = Timer(task_id=task.id)
        timer.start()
        timer.end_time = timer.start_time + timedelta(seconds=10)
        self.assertEqual(timer.duration, 10)

        timer.save()

        timer.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_reset_timer(self):
        """
        Test resetting the timer
        """
        user = User(username="liams",
                    firstname="will",
                    lastname="kub",
                    email="test_email",
                    password="1234")
        user.save()

        project = Project(name="taskmanager",
                          description="Taskmanager project",
                          user_id=user.id)
        project.save()

        task = Task(name="introduction",
                    project_id=project.id,
                    user_id=user.id)
        task.save()

        timer = Timer(task_id=task.id)
        timer.start()
        timer.stop()
        timer.reset()
        self.assertIsNone(timer.end_time)
        self.assertIsNotNone(timer.start_time)
        timer.save()

        timer.delete()
        task.delete()
        project.delete()
        user.delete()
