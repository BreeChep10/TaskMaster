#!/usr/bin/python3
"""
Test Project class
"""
import inspect
import pep8 as pycodestyle
import unittest
from models.project import Project
from models.user import User
from models.task import Task
from models.comment import ProjectComment, TaskComment
import models
module_doc = Project.__doc__


class TestProjectDocs(unittest.TestCase):
    """
    Tests to check documentation of Project class
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup for docstring tests
        """
        cls.project_funcs = inspect.getmembers(Project, inspect.isfunction)

    def test_pep8_comformance(self):
        """
        Test that models/project.py comforms to pep8
        """
        for path in ['models/project.py',
                     'tests/test_models/test_project.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """
        Test for module docstring
        """
        self.assertIsNot(module_doc, None,
                         "Project.py needs a docstring")
        self.assertTrue(len(module_doc) >= 1,
                        "Project class needs a docstring")

    def test_class_docstring(self):
        """
        Tests the Project class docstring
        """
        self.assertIsNot(Project.__doc__, None,
                         "Project class needs a doc string")
        self.assertTrue(len(Project.__doc__) >= 1,
                        "Project class needs a docstring")

    def test_func_docstrings(self):
        """
        Tests the Project class functions docstrings
        """
        for func in self.project_funcs:
            with self.subTest(function=func):
                self.assertIsNot(func[1].__doc__, None,
                                 "{:s} method needs a docstring".
                                 format(func[0]))
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestProject(unittest.TestCase):
    """
    Test the Project class
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

        cls.project_comment = ProjectComment(text="a simple project",
                                             project_id=cls.new_project.id,
                                             user_id=cls.new_user.id)
        cls.project_comment.save()

        print("Classes created")

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class
        """
        try:
            cls.project_comment.delete()
            cls.task_comment.delete()
            cls.new_task.delete()
            cls.new_project.delete()
            cls.new_user.delete()
        except Exception as e:
            models.storage.rollback()
            print(f"Error during teardown: {e}")

    def test_instantiation(self):
        """
        Test the class instantiation using the Project created in setUpClass
        """
        self.assertIs(type(self.new_project), Project)
        print("Project is of type Project")

    def test_attributes(self):
        """
        Test the Project's attributes using the Project created in setUpClass
        """
        self.assertTrue(hasattr(self.new_project, "name"))
        self.assertTrue(hasattr(self.new_project, "description"))
        self.assertTrue(hasattr(self.new_project, "user_id"))
        self.assertTrue(hasattr(self.new_project, "comments"))
        self.assertTrue(hasattr(self.new_project, "tasks"))

    def test_relationships(self):
        """
        Test that Project correctly manages its
        relationships with tasks and comments
        using the Project created in setUpClass
        """
        project = self.new_project
        self.assertIn(self.new_task, project.tasks)
        self.assertIn(self.project_comment, project.comments)

    def test_cascade_delete(self):
        """
        Test that deleting a Project instance
        cascades to delete associated tasks and
        comments using the Project created in setUpClass
        """
        project_id = self.new_project.id
        self.new_project.delete()
        models.storage.save()

        # Ensure project deletion cascades to tasks and comments
        self.assertIsNone(models.storage.get(Project, project_id))
        self.assertIsNone(models.storage.get(Task, self.new_task.id))
        self.assertIsNone(models.storage.get(ProjectComment,
                                             self.project_comment.id))

    def test_project_persistence(self):
        """
        Test that changes to a Project instance are persisted in the database
        """
        new_user = User(username="lee",
                        firstname="williams",
                        lastname="Kubai",
                        password="1234dfad",
                        email="test_email")
        new_project = Project(name="test_project",
                              description="simple_project",
                              user_id=new_user.id)

        new_user.save()
        new_project.save()

        project = models.storage.get(Project, new_project.id)

        project.name = "this is a new name"
        project.save()

        updated_project = models.storage.get(Project, project.id)
        self.assertEqual(updated_project.name, "this is a new name")
        new_user.delete()
        new_project.delete()
