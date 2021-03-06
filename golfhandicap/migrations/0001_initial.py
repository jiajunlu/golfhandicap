# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 19:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=201, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tee', models.CharField(choices=[(b'w', b'White'), (b'u', b'Blue'), (b'b', b'Black'), (b'r', b'Red'), (b'g', b'Gold')], max_length=1)),
                ('course_handicap', models.FloatField(default=0)),
                ('course_slope', models.IntegerField(default=0)),
                ('game_date', models.DateField()),
                ('game_index', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golfhandicap.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default=b'', max_length=200)),
                ('last_name', models.CharField(blank=True, default=b'', max_length=200)),
                ('nick_name', models.CharField(default=b'', max_length=200, unique=True)),
                ('email', models.CharField(blank=True, default=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('adjusted_score', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golfhandicap.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golfhandicap.Player')),
            ],
        ),
    ]
