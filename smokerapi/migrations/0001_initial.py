# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cook',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('controller', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='cook')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='cooks')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('accountType', models.CharField(max_length=100, choices=[('USER', 'User'), ('CONTROLLER', 'Controller')])),
                ('account', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='controllerprofile', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('targetInternalTemp', models.FloatField()),
                ('maxAmbientTemp', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tempAmbient', models.FloatField()),
                ('tempInternal', models.FloatField()),
                ('speedFan', models.IntegerField()),
                ('controller', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sensordata')),
                ('cook', models.ForeignKey(related_name='sensordata', blank=True, to='smokerapi.Cook', null=True)),
            ],
            options={
                'verbose_name': 'Reading',
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='cook',
            name='recipe',
            field=models.ForeignKey(to='smokerapi.Recipe', related_name='cook'),
        ),
    ]
