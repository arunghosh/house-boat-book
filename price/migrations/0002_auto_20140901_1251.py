# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boat', '0001_initial'),
        ('price', '0001_initial'),
    ]

    operations = [
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
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='price',
            name='adult',
            field=models.PositiveIntegerField(verbose_name='Extra cost per adult'),
        ),
        migrations.AlterField(
            model_name='price',
            name='base',
            field=models.PositiveIntegerField(verbose_name='Base Price'),
        ),
        migrations.AlterField(
            model_name='price',
            name='child',
            field=models.PositiveIntegerField(verbose_name='Extra cost per child'),
        ),
    ]
