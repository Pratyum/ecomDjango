# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-24 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0005_auto_20180224_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Incomplete', 'Incomplete'), ('In Progress', 'In Progress'), ('Complete', 'Complete')], max_length=15),
        ),
    ]
