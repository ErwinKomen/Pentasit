# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pentasit', '0003_auto_20160708_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='situation',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]