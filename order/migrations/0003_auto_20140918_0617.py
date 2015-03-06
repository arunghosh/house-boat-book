# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20140904_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=datetime.date(2014, 9, 18), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='date_modified',
            field=models.DateTimeField(default=datetime.date(2014, 9, 18), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
