# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('cancel', '0004_auto_20140902_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='policy',
            name='orders',
            field=models.ManyToManyField(related_name=b'cancel_policies', to='order.Order'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='policy',
            name='boat',
            field=models.ForeignKey(related_name=b'cancel_policies', blank=True, to='boat.Boat', null=True),
        ),
    ]
