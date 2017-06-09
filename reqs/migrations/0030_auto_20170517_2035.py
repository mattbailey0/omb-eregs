# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reqs', '0029_auto_20170517_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencygroup',
            name='agencies',
            field=models.ManyToManyField(blank=True, related_name='groups', to='reqs.Agency'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='agencies',
            field=models.ManyToManyField(blank=True, to='reqs.Agency'),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='agency_groups',
            field=models.ManyToManyField(blank=True, to='reqs.AgencyGroup'),
        ),
    ]
