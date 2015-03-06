# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0003_boat_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='boat',
            name='commission',
            field=models.SmallIntegerField(default=10),
            preserve_default=True,
        ),
    ]
