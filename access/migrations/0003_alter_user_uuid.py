# Generated by Django 5.1.2 on 2024-10-22 18:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.UUID('f81fa10e-0040-4d7a-8df2-8b09d58dbcc1'), editable=False, unique=True, verbose_name='UUID'),
        ),
    ]