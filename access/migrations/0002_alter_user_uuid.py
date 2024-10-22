# Generated by Django 5.1.2 on 2024-10-21 21:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.UUID('e93d781d-754f-45f4-88d1-f7eeb27bc955'), editable=False, unique=True, verbose_name='UUID'),
        ),
    ]