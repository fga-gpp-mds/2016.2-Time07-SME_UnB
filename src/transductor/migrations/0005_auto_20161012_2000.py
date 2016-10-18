# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-12 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transductor', '0004_energytransductor_working_correctly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='energytransductor',
            name='working_correctly',
        ),
        migrations.AddField(
            model_name='energytransductor',
            name='broken',
            field=models.BooleanField(default=False),
        ),
    ]