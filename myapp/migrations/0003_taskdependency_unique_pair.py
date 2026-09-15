from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_taskdependency'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='taskdependency',
            constraint=models.UniqueConstraint(
                fields=('task', 'depends_on'),
                name='unique_task_dependency',
            ),
        ),
    ]
