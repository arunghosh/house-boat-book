# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('specification', models.CharField(max_length=32, null=True, blank=True)),
                ('searchable', models.BooleanField(default=True, verbose_name='Is Searchable')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'amenity',
                'verbose_name_plural': 'amenities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64, verbose_name='Boat Name')),
                ('no_room', models.PositiveSmallIntegerField(default=2, verbose_name='No of rooms')),
                ('type', models.SmallIntegerField(default=1, choices=[(1, b'Luxury'), (2, b'Premium'), (3, b'Deluxe')])),
                ('ac_type', models.SmallIntegerField(verbose_name='A/C types', choices=[(1, b'Full Time AC'), (2, b'Partial AC'), (3, b'Non AC')])),
                ('no_adult', models.PositiveIntegerField(default=2, verbose_name='Number of customers')),
                ('max_adult', models.PositiveIntegerField(default=4, verbose_name='Max number customers')),
                ('max_child', models.PositiveIntegerField(default=4, verbose_name='Max allowed children')),
                ('status', models.SmallIntegerField(verbose_name='Boat Status', choices=[(0, b'Active'), (0, b'Maintenance'), (0, b'Removed')])),
                ('amenities', models.ManyToManyField(to='boat.Amenity', null=True, blank=True)),
                ('company', models.ForeignKey(related_name=b'boats', to='company.Company')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=b'boat_images')),
                ('description', models.CharField(max_length=256)),
                ('is_primary', models.BooleanField(default=False)),
                ('boat', models.ForeignKey(related_name=b'images', to='boat.Boat')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
