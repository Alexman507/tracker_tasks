from django.contrib import admin

from tasker.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at", "tag", "parent_task", "deadline", "status",
                    "responsible_manager", "priority", "is_active")

admin.site.register(Task, TaskAdmin)
