# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_baseuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='type',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, b'Unknown'), (2, b'Agent'), (4, b'Boats ok Kerala'), (1, b'Customer'), (3, b'Owner')]),
        ),
    ]
