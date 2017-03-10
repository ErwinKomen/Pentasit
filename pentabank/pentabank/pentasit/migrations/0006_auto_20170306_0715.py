# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-06 06:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pentasit', '0005_auto_20160708_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='example',
            name='situation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='example12m_situation', to='pentasit.Situation'),
        ),
        migrations.AddField(
            model_name='node',
            name='situation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='node12m_situation', to='pentasit.Situation'),
        ),
        migrations.AddField(
            model_name='nptype',
            name='node',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='nptype12m_node', to='pentasit.Node'),
        ),
        migrations.AddField(
            model_name='word',
            name='node',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='word12m_node', to='pentasit.Node'),
        ),
        migrations.AlterField(
            model_name='node',
            name='npType',
            field=models.ManyToManyField(blank=True, default=1, related_name='nodem2m_npType', to='pentasit.NpType'),
        ),
        migrations.AlterField(
            model_name='node',
            name='word',
            field=models.ManyToManyField(blank=True, default=1, related_name='nodem2m_word', to='pentasit.Word'),
        ),
        migrations.AlterField(
            model_name='nptype',
            name='name',
            field=models.CharField(choices=[('6', 'AnchoredNP'), ('5', 'Bare'), ('1', 'DefNP'), ('4', 'DemNP'), ('7', 'FullNP'), ('2', 'IndefNP'), ('3', 'QuantNP')], default='0', help_text='Sorry, no help available for situation.npType', max_length=5, verbose_name='NP type'),
        ),
        migrations.AlterField(
            model_name='situation',
            name='example',
            field=models.ManyToManyField(default=1, related_name='situationm2m_example', to='pentasit.Example'),
        ),
        migrations.AlterField(
            model_name='situation',
            name='nodes',
            field=models.ManyToManyField(blank=True, default=1, related_name='situationm2m_node', to='pentasit.Node'),
        ),
        migrations.AlterField(
            model_name='situation',
            name='npType',
            field=models.CharField(choices=[('6', 'AnchoredNP'), ('5', 'Bare'), ('1', 'DefNP'), ('4', 'DemNP'), ('7', 'FullNP'), ('2', 'IndefNP'), ('3', 'QuantNP')], default='0', help_text='Sorry, no help available for situation.npType', max_length=5, verbose_name='NP type'),
        ),
    ]