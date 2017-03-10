# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-10 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pentasit', '0008_auto_20170310_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='example',
            name='situation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='pentasit.Situation'),
        ),
        migrations.AlterField(
            model_name='node',
            name='situation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='nodes', to='pentasit.Situation'),
        ),
    ]
