# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-05 23:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20161106_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateField(),
        ),
    ]
