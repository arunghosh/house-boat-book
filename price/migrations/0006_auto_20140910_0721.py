# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0005_auto_20140910_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasonprice',
            name='date_from',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='seasonprice',
            name='date_to',
            field=models.DateField(),
        ),
    ]
