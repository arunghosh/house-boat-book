# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0003_auto_20140901_1256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='price',
            name='is_primary',
        ),
    ]
