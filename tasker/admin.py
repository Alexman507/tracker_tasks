from tasker.models import Task
from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at", "tag", "parent_task", "deadline", "status",
                    "responsible_manager", "priority", "is_active")

admin.site.register(Task, TaskAdmin)
