# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-01-30 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(default=None, max_length=40)),
                ('user_image', models.CharField(max_length=255, null=True)),
                ('province', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(max_length=255, null=True)),
                ('nickname', models.CharField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=255, null=True)),
                ('is_subscribe', models.IntegerField(default=0, null=True)),
                ('subscribe_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_member', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(default=None, max_length=40)),
                ('hashcode', models.CharField(max_length=255, null=True)),
                ('hashName', models.CharField(max_length=1024, null=True)),
            ],
        ),
    ]
