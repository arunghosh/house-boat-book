# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boat',
            name='status',
        ),
        migrations.AddField(
            model_name='boat',
            name='is_bok',
            field=models.BooleanField(default=True, verbose_name='Is available to BoK'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='boat',
            name='max_adult',
            field=models.PositiveIntegerField(default=4, verbose_name='Max number adults'),
        ),
        migrations.AlterField(
            model_name='boat',
            name='no_adult',
            field=models.PositiveIntegerField(default=2, verbose_name='Number of adults'),
        ),
    ]
