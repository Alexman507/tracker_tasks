# Generated by Django 4.2.15 on 2024-09-15 18:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasker', '0007_remove_task_insert_insert_remove_task_update_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ManyToManyField(related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='исполнители'),
        ),
    ]
