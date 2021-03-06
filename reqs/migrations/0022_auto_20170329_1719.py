# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reqs', '0021_auto_20170321_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='citation',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='impacted_entity',
            field=models.CharField(blank=True, max_length=8192),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='policy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reqs.Policy'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='policy_section',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='policy_sub_section',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='req_deadline',
            field=models.CharField(blank=True, max_length=512),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='verb',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
