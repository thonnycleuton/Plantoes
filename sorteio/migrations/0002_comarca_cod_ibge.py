# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-11 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comarca',
            name='cod_ibge',
            field=models.CharField(default='2211001', max_length=8),
            preserve_default=False,
        ),
    ]
