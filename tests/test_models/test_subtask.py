#!/usr/bin/python3
"""
Test Subtask class
"""
import inspect
import pep8 as pycodestyle
import unittest
from models.subtask import Subtask
from models.task import Task
from models.user import User
from models.project import Project
import models


class TestSubtaskDocs(unittest.TestCase):
    """
    Tests to check documentation of Subtask class
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup for docstring tests
        """
        cls.subtask_funcs = inspect.getmembers(Subtask, inspect.isfunction)

    def test_pep8_conformance(self):
        """
        Test that models/subtask.py conforms to PEP8
        """
        for path in ['models/subtask.py',
                     'tests/test_models/test_subtask.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(Subtask.__doc__, None,
                         "subtask.py needs a docstring")
        self.assertTrue(len(Subtask.__doc__) >= 1,
                        "Subtask class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the Subtask class docstring
        """
        self.assertIsNot(Subtask.__doc__, None,
                         "Subtask class needs a doc string")
        self.assertTrue(len(Subtask.__doc__) >= 1,
                        "Subtask class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the Subtask class functions docstrings
        """
        for func in self.subtask_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestSubtask(unittest.TestCase):
    """
    Test the Subtask class
    """

    def test_instantiation(self):
        """
        Test the class instantiation
        """
        new_user = User(username="liams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")
        new_user.save()

        new_task = Task(name="introduction",
                        user_id=new_user.id)
        new_task.save()

        new_subtask = Subtask(name="setup environment",
                              description="Set up dev environment",
                              task_id=new_task.id)
        new_subtask.save()

        self.assertIs(type(new_subtask), Subtask)
        print("Subtask is of type Subtask")

        # Clean up
        new_subtask.delete()
        new_task.delete()
        new_user.delete()

    def test_attributes(self):
        """
        Test the Subtask's attributes
        """
        new_user = User(username="liams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")
        new_user.save()

        new_task = Task(name="introduction",
                        user_id=new_user.id)
        new_task.save()

        new_subtask = Subtask(name="setup environment",
                              description="Set up dev environment",
                              task_id=new_task.id)
        new_subtask.save()

        self.assertTrue(hasattr(new_subtask, "name"))
        self.assertTrue(hasattr(new_subtask, "description"))
        self.assertTrue(hasattr(new_subtask, "task_id"))
        self.assertTrue(hasattr(new_subtask, "subtaskstatus"))
        self.assertTrue(hasattr(new_subtask, "subtaskpriority"))

        # Clean up
        new_subtask.delete()
        new_task.delete()
        new_user.delete()

    def test_relationships(self):
        """
        Test the relationship between Task and Subtask
        """
        new_user = User(username="liams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")
        new_user.save()

        new_task = Task(name="introduction",
                        user_id=new_user.id)
        new_task.save()

        new_subtask = Subtask(name="setup environment",
                              description="Set up dev environment",
                              task_id=new_task.id)
        new_subtask.save()

        self.assertIn(new_subtask, new_task.subtasks)

        # Clean up
        new_subtask.delete()
        new_task.delete()
        new_user.delete()

    def test_subtask_persistence(self):
        """
        Test that changes to a Subtask instance are persisted in the database
        """
        new_user = User(username="liams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")
        new_user.save()

        new_task = Task(name="introduction",
                        user_id=new_user.id)
        new_task.save()

        new_subtask = Subtask(name="setup environment",
                              description="Set up dev environment",
                              task_id=new_task.id)
        new_subtask.save()

        new_subtask.name = "Configure IDE"
        new_subtask.save()

        updated_subtask = models.storage.get(Subtask, new_subtask.id)
        self.assertEqual(updated_subtask.name, "Configure IDE")

        # Clean up
        new_subtask.delete()
        new_task.delete()
        new_user.delete()

    def test_name_not_nullable(self):
        """
        Test that the name attribute is not nullable
        new_user = User(username="liams",
                        firstname="will",
                        lastname="kub",
                        email="test_email",
                        password="1234")
        new_user.save()

        new_task = Task(name="introduction",
                        user_id=new_user.id)
        new_task.save()

        with self.assertRaises(Exception):
            Subtask(name=None, task_id=new_task.id).save()

        # Clean up
        new_task.delete()
        new_user.delete()
        """
        pass

    def test_cascade_delete(self):
        """
        Test that deleting a Task instance cascades
        to delete associated Subtasks
        """
        new_user = User(username="lee",
                        firstname="williams",
                        lastname="Kubai",
                        password="1234dfad",
                        email="test_email")
        new_user.save()
        new_project = Project(name="test_project",
                              description="simple_project",
                              user_id=new_user.id)
        new_project.save()
        new_task = Task(name="test_task",
                        project_id=new_project.id,
                        user_id=new_user.id)
        new_task.save()
        new_subtask = Subtask(name="test_subtask",
                              task_id=new_task.id)
        new_subtask.save()
        task_id = new_task.id
        new_task.delete()
        models.storage.save()
        self.assertIsNone(models.storage.get(Task, task_id))
        self.assertIsNone(models.storage.get(Subtask, new_subtask.id))

        # Clean up
        new_project.delete()
        new_user.delete()
