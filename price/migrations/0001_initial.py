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
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_from', models.DateField(null=True, blank=True)),
                ('date_to', models.DateField(null=True, blank=True)),
                ('base', util.modelfields.CurrencyField(verbose_name='Base Price', max_digits=10, decimal_places=2)),
                ('adult', models.IntegerField(verbose_name='Extra cost per adult')),
                ('child', models.IntegerField(verbose_name='Extra cost per child')),
                ('is_active', models.BooleanField(default=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('boat', models.ForeignKey(related_name=b'prices', to='boat.Boat')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
