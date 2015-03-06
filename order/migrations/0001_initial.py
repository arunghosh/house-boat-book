# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import util.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0003_auto_20140901_1256'),
        ('boat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('no_adult', models.PositiveSmallIntegerField(default=0)),
                ('no_child', models.PositiveSmallIntegerField(default=0)),
                ('cost_original', util.modelfields.CurrencyField(default=0, max_digits=10, decimal_places=2)),
                ('cost_final', util.modelfields.CurrencyField(default=0, max_digits=10, decimal_places=2)),
                ('is_veg', models.BooleanField(default=False, verbose_name='Is vegetarian cuisine')),
                ('require_pick', models.BooleanField(default=False, verbose_name='Require pick and drop')),
                ('agreed_terms', models.BooleanField(default=False)),
                ('order_status', models.SmallIntegerField(default=0, choices=[(0, 'Initial'), (10, 'Confirmed'), (15, 'Travelled'), (20, 'Cancelled')])),
                ('date_in', models.DateField()),
                ('date_out', models.DateField()),
                ('date_confirm', models.DateField(null=True, blank=True)),
                ('source', models.SmallIntegerField(default=1)),
                ('is_active', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('boat', models.ForeignKey(related_name=b'orders', to='boat.Boat')),
                ('customer', models.ForeignKey(related_name=b'orders', to='order.Customer')),
                ('price', models.ForeignKey(related_name=b'orders', to='price.Price', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateTimeField()),
                ('text', models.CharField(max_length=256)),
                ('order', models.ForeignKey(related_name=b'comments', to='order.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
