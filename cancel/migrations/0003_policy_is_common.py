# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cancel', '0002_cancel_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='is_common',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
