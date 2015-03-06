# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0003_boat_price'),
        ('price', '0004_remove_price_is_primary'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_from', models.DateField(null=True, blank=True)),
                ('date_to', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('boat', models.ForeignKey(related_name=b'season_prices', to='boat.Boat')),
                ('price', models.ForeignKey(to='price.Price')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='price',
            name='boat',
        ),
        migrations.RemoveField(
            model_name='price',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='price',
            name='date_from',
        ),
        migrations.RemoveField(
            model_name='price',
            name='date_modified',
        ),
        migrations.RemoveField(
            model_name='price',
            name='date_to',
        ),
        migrations.RemoveField(
            model_name='price',
            name='is_active',
        ),
    ]
