# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('amount', util.modelfields.CurrencyField(max_digits=10, decimal_places=2)),
                ('ip_address', models.GenericIPAddressField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('days', models.PositiveSmallIntegerField()),
                ('percent', models.PositiveSmallIntegerField()),
                ('boat', models.ForeignKey(related_name=b'cancel_policies', to='boat.Boat')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
