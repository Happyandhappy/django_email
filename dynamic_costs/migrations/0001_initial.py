# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0010_auto_20141112_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('from_date', models.DateField(verbose_name='From date')),
                ('to_date', models.DateField(verbose_name='To date')),
                ('common_information', models.TextField(null=True, verbose_name='Common information', blank=True)),
                ('entrance', select2.fields.ForeignKey(to='entrances.Entrance')),
            ],
            options={
                'verbose_name': 'Dynamic cost',
                'verbose_name_plural': 'Dynamic costs',
            },
            bases=(models.Model,),
        ),
    ]
