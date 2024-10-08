# Generated by Django 4.2.15 on 2024-09-12 21:53

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0004_alter_task_tag_alter_taskevent_tag'),
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
            name='is_important',
        ),
        migrations.RemoveField(
            model_name='taskevent',
            name='is_important',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='insert_insert', sql=pgtrigger.compiler.UpsertTriggerSql(func='INSERT INTO "tasker_taskevent" ("deadline", "executor_id", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."executor_id", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'insert\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='46692019edfc9dd2edf4db8417e2451befdf4073', operation='INSERT', pgid='pgtrigger_insert_insert_78725', table='tasker_task', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='task',
            trigger=pgtrigger.compiler.Trigger(name='update_update', sql=pgtrigger.compiler.UpsertTriggerSql(condition='WHEN (OLD.* IS DISTINCT FROM NEW.*)', func='INSERT INTO "tasker_taskevent" ("deadline", "executor_id", "id", "is_active", "name", "notes", "parent_task_id", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "priority", "responsible_manager_id", "status", "tag", "updated_at") VALUES (NEW."deadline", NEW."executor_id", NEW."id", NEW."is_active", NEW."name", NEW."notes", NEW."parent_task_id", _pgh_attach_context(), NOW(), \'update\', NEW."id", NEW."priority", NEW."responsible_manager_id", NEW."status", NEW."tag", NEW."updated_at"); RETURN NULL;', hash='6150885902072215af4346cf9ccb922e61eba86e', operation='UPDATE', pgid='pgtrigger_update_update_48fa8', table='tasker_task', when='AFTER')),
        ),
    ]
