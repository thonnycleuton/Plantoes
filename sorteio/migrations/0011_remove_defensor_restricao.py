# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-07 17:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sorteio', '0010_defensor_restricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defensor',
            name='restricao',
        ),
    ]
