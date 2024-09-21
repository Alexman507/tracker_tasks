# Generated by Django 4.2.15 on 2024-09-15 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasker', '0009_alter_task_executor'),
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
        migrations.AddField(
            model_name='taskevent',
            name='executor',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, parent_link='users.User.tasks', related_name='+', related_query_name='+', to=settings.AUTH_USER_MODEL, verbose_name='исполнители'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='executor',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='insert_insert', sql=pgtrigger.compiler.UpsertTriggerSql(func='INSERT INTO "tasker_taskevent" ("deadline", "executor_id", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."executor_id", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='46692019edfc9dd2edf4db8417e2451befdf4073', operation='INSERT', pgid='pgtrigger_insert_insert_78725', table='tasker_task', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='update_update', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func='INSERT INTO "tasker_taskevent" ("deadline", "executor_id", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."executor_id", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='6150885902072215af4346cf9ccb922e61eba86e', operation='UPDATE', pgid='pgtrigger_update_update_48fa8', table='tasker_task', when='AFTER')),
        ),
        migrations.AddField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, parent_link='users.User.tasks', related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='исполнители'),
        ),
    ]
