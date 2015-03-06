# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0003_boat_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('boat', models.ForeignKey(to='boat.Boat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
