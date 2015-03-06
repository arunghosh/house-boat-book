# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0001_initial'),
        ('order', '0001_initial'),
        ('cancel', '0005_auto_20140902_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoatCancelPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.PositiveSmallIntegerField()),
                ('percent', models.PositiveSmallIntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('boat', models.ForeignKey(related_name=b'cancel_policies', blank=True, to='boat.Boat', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderCancelPolicy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.PositiveSmallIntegerField()),
                ('percent', models.PositiveSmallIntegerField()),
                ('order', models.ForeignKey(related_name=b'cancel_policies', to='order.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='policy',
            name='boat',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='orders',
        ),
        migrations.DeleteModel(
            name='Policy',
        ),
    ]
