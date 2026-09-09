from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Task, TaskDependency


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
