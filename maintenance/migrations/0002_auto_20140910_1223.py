# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='date_created',
            field=models.DateTimeField(default=datetime.date(2014, 9, 10), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='maintenance',
            name='date_modified',
            field=models.DateTimeField(default=datetime.date(2014, 9, 10), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='boat',
            field=models.ForeignKey(related_name=b'maintenance', to='boat.Boat'),
        ),
    ]
