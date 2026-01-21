from django.db import models
from django.core.exceptions import ValidationError


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def update_status_based_on_dependencies(self):
        """
        Auto-update task status based on dependencies.
        """
        dependencies = self.dependencies.all()

        if not dependencies.exists():
            return

        for dep in dependencies:
            if dep.depends_on.status != 'completed':
                self.status = 'pending'
                self.save()
                return

        self.status = 'in_progress'
        self.save()

    def has_circular_dependency(self, target_task):
        """
        Detect circular dependency using DFS.
        """
        visited = set()

        def dfs(task):
            if task.id in visited:
                return False
            visited.add(task.id)

            if task == self:
                return True

            for dep in task.dependencies.all():
                if dfs(dep.depends_on):
                    return True
            return False

        return dfs(target_task)


class TaskDependency(models.Model):
    task = models.ForeignKey(
        Task,
        related_name='dependencies',
        on_delete=models.CASCADE
    )
    depends_on = models.ForeignKey(
        Task,
        related_name='dependents',
        on_delete=models.CASCADE
    )

    def clean(self):
        if self.task == self.depends_on:
            raise ValidationError("A task cannot depend on itself.")

        if self.task.has_circular_dependency(self.depends_on):
            raise ValidationError("Circular dependency detected.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task.title} depends on {self.depends_on.title}"
