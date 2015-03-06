# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('cancel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancel',
            name='order',
            field=models.OneToOneField(to='order.Order'),
            preserve_default=True,
        ),
    ]
