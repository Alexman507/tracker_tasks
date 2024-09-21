from django.db.models import Count

from tasker.models import Task
from users.models import User


def free_executor_get_queryset():
    user_min_task = (
        User.objects.all()
        .annotate(task_count=Count("tasks"))
        .order_by("task_count")
        .first()
    )
    task_parent = Task.objects.filter(parent_task__isnull=False, executors=None).first()
    user_task_parent = User.objects.filter(tasks__id=task_parent.id).first()
    count_user_task_parent = len(list(user_task_parent.tasks.all()))
    count_user_min_task = len(list(user_min_task.tasks.all()))
    if count_user_task_parent - count_user_min_task <= 2:
        queryset = User.objects.filter(pk=user_task_parent.pk)
    else:
        queryset = User.objects.filter(pk=user_min_task.pk)

    return queryset
