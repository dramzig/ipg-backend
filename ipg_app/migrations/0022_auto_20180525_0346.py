# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-25 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipg_app', '0021_auto_20180525_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ipg_app.Country'),
        ),
        migrations.AddField(
            model_name='profile',
            name='operator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ipg_app.Operator'),
        ),
    ]
