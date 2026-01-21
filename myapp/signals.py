from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TaskDependency


@receiver(post_save, sender=TaskDependency)
def update_task_status_on_dependency_change(sender, instance, **kwargs):
    """
    Automatically update task status when a dependency is added or changed.
    """
    task = instance.task
    task.update_status_based_on_dependencies()
