# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-13 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0023_auto_20161123_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServingAutoUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='serving',
            name='date_served',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='ref_cycle_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='vendorservice',
            name='end_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='vendorservice',
            name='start_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='servingautoupdate',
            name='timetable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetables.Timetable'),
        ),
        migrations.AddField(
            model_name='servingautoupdate',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetables.Vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='servingautoupdate',
            unique_together=set([('timetable', 'vendor', 'date')]),
        ),
    ]
