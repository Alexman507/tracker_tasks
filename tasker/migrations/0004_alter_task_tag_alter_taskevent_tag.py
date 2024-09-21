# Generated by Django 4.2.15 on 2024-09-11 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasker', '0003_remove_task_insert_insert_remove_task_update_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='tag',
            field=models.CharField(blank=True, choices=[('purchase', 'Закупка'), ('spare parts', 'Запчасти'), ('modification', 'Модификация'), ('service', 'Обслуживание'), ('education', 'Обучение'), ('offer', 'Предложение'), ('development', 'Разработка')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='taskevent',
            name='tag',
            field=models.CharField(blank=True, choices=[('purchase', 'Закупка'), ('spare parts', 'Запчасти'), ('modification', 'Модификация'), ('service', 'Обслуживание'), ('education', 'Обучение'), ('offer', 'Предложение'), ('development', 'Разработка')], max_length=20, null=True),
        ),
    ]
