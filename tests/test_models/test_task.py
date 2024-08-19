#!/usr/bin/python3
"""
Test Task class
"""
import inspect
import pep8 as pycodestyle
import unittest
from models.task import Task
from models.user import User
from models.project import Project
from models.comment import TaskComment
import models
module_doc = Task.__doc__


class TestTaskDocs(unittest.TestCase):
    """
    Tests to check documentation of Task class
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup for docstring tests
        """
        cls.task_funcs = inspect.getmembers(Task, inspect.isfunction)

    def test_pep8_comformance(self):
        """
        Test that models/task.py conforms to pep8
        """
        for path in ['models/task.py',
                     'tests/test_models/test_task.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(module_doc, None,
                         "Task.py needs a docstring")
        self.assertTrue(len(module_doc) >= 1,
                        "Task class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the Task class docstring
        """
        self.assertIsNot(Task.__doc__, None,
                         "Task class needs a doc string")
        self.assertTrue(len(Task.__doc__) >= 1,
                        "Task class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the Task class functions docstrings
        """
        for func in self.task_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestTask(unittest.TestCase):
    """
    Test the Task class
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.new_user = User(username="liams",
                            firstname="will",
                            lastname="kub",
                            email="test_email",
                            password="1234")
        cls.new_user.save()

        cls.new_project = Project(name="taskmanager",
                                  description="Taskmanager project",
                                  user_id=cls.new_user.id)
        cls.new_project.save()

        cls.new_task = Task(name="introduction",
                            project_id=cls.new_project.id,
                            user_id=cls.new_user.id)
        cls.new_task.save()

        cls.task_comment = TaskComment(text="simple task",
                                       user_id=cls.new_user.id,
                                       task_id=cls.new_task.id)
        cls.task_comment.save()

        print("Classes created")

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class
        """
        try:
            cls.task_comment.delete()
            cls.new_task.delete()
            cls.new_project.delete()
            cls.new_user.delete()
        except Exception as e:
            models.storage.rollback()
            print(f"Error during teardown: {e}")

    def test_instantiation(self):
        """
        Test the class instantiation using the Task created in setUpClass
        """
        self.assertIs(type(self.new_task), Task)
        print("Task is of type Task")

    def test_attributes(self):
        """
        Test the Task's attributes using the Task created in setUpClass
        """
        self.assertTrue(hasattr(self.new_task, "name"))
        self.assertTrue(hasattr(self.new_task, "description"))
        self.assertTrue(hasattr(self.new_task, "project_id"))
        self.assertTrue(hasattr(self.new_task, "user_id"))
        self.assertTrue(hasattr(self.new_task, "comments"))
        self.assertTrue(hasattr(self.new_task, "subtasks"))
        self.assertTrue(hasattr(self.new_task, "timers"))
        self.assertTrue(hasattr(self.new_task, "taskstatus"))
        self.assertTrue(hasattr(self.new_task, "taskpriority"))
        self.assertTrue(hasattr(self.new_task, "taskprogress"))

    def test_relationships(self):
        """
        Test that Task correctly manages its relationships
        with comments, subtasks, and timers using
        the Task created in setUpClass
        """
        task = self.new_task
        self.assertIn(self.task_comment, task.comments)
        # Add similar assertions for subtasks and timers if any

    def test_cascade_delete(self):
        """
        Test that deleting a Task instance cascades to delete
        associated comments, subtasks, and timers using
        the Task created in setUpClass
        """
        task_id = self.new_task.id
        self.new_task.delete()
        models.storage.save()

        # Ensure task deletion cascades to comments, subtasks, and timers
        self.assertIsNone(models.storage.get(Task, task_id))
        self.assertIsNone(models.storage.get(
            TaskComment, self.task_comment.id))
        # Add similar assertions for subtasks and timers if any

    def test_task_persistence(self):
        """
        Test that changes to a Task instance are persisted in the database
        """
        new_task = Task(name="test_task",
                        description="simple_task",
                        project_id=self.new_project.id,
                        user_id=self.new_user.id)
        new_task.save()

        task = models.storage.get(Task, new_task.id)

        task.name = "this is a new name"
        task.save()

        updated_task = models.storage.get(Task, task.id)
        self.assertEqual(updated_task.name, "this is a new name")
        task.delete()
