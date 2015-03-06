# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20140918_0617'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commission',
            field=models.SmallIntegerField(default=10),
            preserve_default=True,
        ),
    ]
