# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cancel', '0003_policy_is_common'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='is_common',
        ),
        migrations.AlterField(
            model_name='policy',
            name='boat',
            field=models.ForeignKey(related_name=b'cancel_policies', to='boat.Boat', null=True),
        ),
    ]
