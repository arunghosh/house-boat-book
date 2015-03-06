# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0002_auto_20140901_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='boat',
        ),
        migrations.DeleteModel(
            name='Policy',
        ),
    ]
