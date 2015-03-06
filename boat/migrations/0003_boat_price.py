# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0004_remove_price_is_primary'),
        ('boat', '0002_auto_20140909_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='boat',
            name='price',
            field=models.ForeignKey(related_name=b'boats', default=1, to='price.Price'),
            preserve_default=False,
        ),
    ]
