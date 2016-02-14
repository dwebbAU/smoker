# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cook',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('controller', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='cook')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='cooks')),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('speedFan', models.IntegerField()),
                ('controller', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='instruction')),
                ('cook', models.ForeignKey(to='smokerapi.Cook', related_name='instruction')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.TextField()),
                ('max_temp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tempAmbient', models.FloatField()),
                ('tempInternal', models.FloatField()),
                ('speedFan', models.IntegerField()),
                ('controller', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sensordata')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='cook',
            name='recipe',
            field=models.ForeignKey(to='smokerapi.Recipe', related_name='cook'),
        ),
    ]
