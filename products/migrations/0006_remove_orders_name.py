# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 18:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20170316_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='name',
        ),
    ]
