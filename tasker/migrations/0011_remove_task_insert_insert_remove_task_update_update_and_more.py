# Generated by Django 4.2.15 on 2024-09-15 19:00

from django.conf import settings
from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasker', '0010_remove_task_insert_insert_remove_task_update_update_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='task',
            name='insert_insert',
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name='task',
            name='update_update',
        ),
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        migrations.RemoveField(
            model_name='taskevent',
            name='executor',
        ),
        migrations.AddField(
            model_name='task',
            name='executors',
            field=models.ManyToManyField(blank=True, related_name='executors', to=settings.AUTH_USER_MODEL, verbose_name='исполнители'),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='insert_insert', sql=pgtrigger.compiler.UpsertTriggerSql(func='INSERT INTO "tasker_taskevent" ("deadline", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='8d5c5562f1ec865a7119d614558eee51f950ee8b', operation='INSERT', pgid='pgtrigger_insert_insert_78725', table='tasker_task', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='update_update', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func='INSERT INTO "tasker_taskevent" ("deadline", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='86f7414787e8843c6c17f2e9eb160d8770e47c1d', operation='UPDATE', pgid='pgtrigger_update_update_48fa8', table='tasker_task', when='AFTER')),
        ),
    ]
