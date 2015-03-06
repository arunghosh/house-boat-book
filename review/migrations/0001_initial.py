# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20140904_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('comment', models.CharField(max_length=512)),
                ('cleanliness', models.PositiveSmallIntegerField()),
                ('food', models.PositiveSmallIntegerField()),
                ('ambience', models.PositiveSmallIntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('order', models.ForeignKey(related_name=b'reviews', to='order.Order')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
