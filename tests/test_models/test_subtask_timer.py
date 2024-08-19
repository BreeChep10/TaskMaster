"""
Test SubtaskTimer class
"""
import inspect
import pep8 as pycodestyle
import unittest
from datetime import timedelta
from models.timer import SubtaskTimer
from models.subtask import Subtask
from models.user import User
from models.project import Project
from models.task import Task
import models

module_doc = SubtaskTimer.__doc__


class TestSubtaskTimerDocs(unittest.TestCase):
    """
    Tests to check documentation of SubtaskTimer class
    """

    def setUp(self):
        """
        Setup for docstring tests
        """
        self.subtask_timer_funcs = inspect.getmembers(
            SubtaskTimer,
            inspect.isfunction)

    def test_pep8_conformance(self):
        """
        Test that models/subtask_timer.py conforms to pep8
        """
        for path in ['models/timer.py',
                     'tests/test_models/test_subtask_timer.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(module_doc, None,
                         "subtask_timer.py needs a docstring")
        self.assertTrue(len(module_doc) >= 1,
                        "SubtaskTimer class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the SubtaskTimer class docstring
        """
        self.assertIsNot(SubtaskTimer.__doc__, None,
                         "SubtaskTimer class needs a doc string")
        self.assertTrue(len(SubtaskTimer.__doc__) >= 1,
                        "SubtaskTimer class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the SubtaskTimer class functions docstrings
        """
        for func in self.subtask_timer_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestSubtaskTimer(unittest.TestCase):
    """
    Test the SubtaskTimer class
    """

    def test_instantiation(self):
        """
        Test the class instantiation using SubtaskTimer
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

        subtask = Subtask(name="subtask intro",
                          task_id=task.id)
        subtask.save()

        subtask_timer = SubtaskTimer(subtask_id=subtask.id)
        subtask_timer.save()

        self.assertIs(type(subtask_timer), SubtaskTimer)
        subtask_timer.delete()
        subtask.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_start_subtask_timer(self):
        """
        Test starting the subtask timer
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

        subtask = Subtask(name="subtask intro",
                          task_id=task.id)
        subtask.save()

        subtask_timer = SubtaskTimer(subtask_id=subtask.id)
        subtask_timer.start()
        self.assertIsNotNone(subtask_timer.start_time)
        subtask_timer.save()

        subtask_timer.delete()
        subtask.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_stop_subtask_timer(self):
        """
        Test stopping the subtask timer
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

        subtask = Subtask(name="subtask intro",
                          task_id=task.id)
        subtask.save()

        subtask_timer = SubtaskTimer(subtask_id=subtask.id)
        subtask_timer.start()
        subtask_timer.stop()
        self.assertIsNotNone(subtask_timer.end_time)
        subtask_timer.save()

        subtask_timer.delete()
        subtask.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_subtask_timer_duration(self):
        """
        Test calculating the duration of the subtask timer
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

        subtask = Subtask(name="subtask intro",
                          task_id=task.id)
        subtask.save()

        subtask_timer = SubtaskTimer(subtask_id=subtask.id)
        subtask_timer.start()
        subtask_timer.end_time = subtask_timer.\
            start_time + timedelta(seconds=15)
        self.assertEqual(subtask_timer.duration, 15)
        subtask_timer.save()

        subtask_timer.delete()
        subtask.delete()
        task.delete()
        project.delete()
        user.delete()

    def test_reset_subtask_timer(self):
        """
        Test resetting the subtask timer
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

        subtask = Subtask(name="subtask intro",
                          task_id=task.id)
        subtask.save()

        subtask_timer = SubtaskTimer(subtask_id=subtask.id)
        subtask_timer.start()
        subtask_timer.stop()
        subtask_timer.reset()
        self.assertIsNone(subtask_timer.end_time)
        self.assertIsNotNone(subtask_timer.start_time)
        subtask_timer.save()

        subtask_timer.delete()
        subtask.delete()
        task.delete()
        project.delete()
        user.delete()
