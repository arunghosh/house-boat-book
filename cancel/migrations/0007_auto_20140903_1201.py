# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cancel', '0006_auto_20140902_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cancel',
            old_name='amount',
            new_name='amount_cancel',
        ),
        migrations.AddField(
            model_name='cancel',
            name='amount_refund',
            field=util.modelfields.CurrencyField(default=0, max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
    ]
