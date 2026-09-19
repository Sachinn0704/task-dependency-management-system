from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .models import Task, TaskDependency
from .views import task_api


class TaskDependencyModelTests(TestCase):
    def setUp(self):
        self.first = Task.objects.create(title="First task")
        self.second = Task.objects.create(title="Second task")

    def test_task_string_representation(self):
        self.assertEqual(str(self.first), "First task")

    def test_self_dependency_is_rejected(self):
        dependency = TaskDependency(task=self.first, depends_on=self.first)

        with self.assertRaises(ValidationError):
            dependency.save()

    def test_circular_dependency_is_rejected(self):
        TaskDependency.objects.create(task=self.first, depends_on=self.second)
        dependency = TaskDependency(task=self.second, depends_on=self.first)

        with self.assertRaises(ValidationError):
            dependency.save()

    def test_duplicate_dependency_is_rejected_by_database_constraint(self):
        TaskDependency.objects.create(task=self.first, depends_on=self.second)

        with self.assertRaises(IntegrityError):
            TaskDependency.objects.create(task=self.first, depends_on=self.second)

    def test_pending_task_becomes_in_progress_when_dependencies_are_complete(self):
        TaskDependency.objects.create(task=self.first, depends_on=self.second)
        self.second.status = "completed"
        self.second.save(update_fields=["status"])

        self.first.update_status_based_on_dependencies()
        self.first.refresh_from_db()

        self.assertEqual(self.first.status, "in_progress")

    def test_task_stays_pending_when_dependency_is_not_complete(self):
        TaskDependency.objects.create(task=self.first, depends_on=self.second)

        self.first.status = "in_progress"
        self.first.save(update_fields=["status"])
        self.first.update_status_based_on_dependencies()
        self.first.refresh_from_db()

        self.assertEqual(self.first.status, "pending")


class TaskApiFilterTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Task.objects.create(title="Pending task", status="pending")
        Task.objects.create(title="Done task", status="completed")

    def test_status_filter_returns_matching_tasks(self):
        request = self.factory.get('/api/tasks/', {'status': 'completed'})
        response = task_api(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'completed')

    def test_invalid_status_filter_returns_allowed_values(self):
        request = self.factory.get('/api/tasks/', {'status': 'blocked_by_unknown'})
        response = task_api(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn('allowed_statuses', response.data)
