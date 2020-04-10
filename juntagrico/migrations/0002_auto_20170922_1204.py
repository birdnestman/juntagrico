# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 10:04
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityarea',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='share',
            name='member',
            field=models.ForeignKey(
                blank=True, on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
    ]
