# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import select2.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0013_auto_20141112_1337'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0017_remove_task_is_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_date', models.DateField(default=datetime.date.today, verbose_name='From date')),
                ('to_date', models.DateField(default=datetime.date.today, verbose_name='To date')),
                ('assignee', select2.fields.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('entrance', select2.fields.ForeignKey(verbose_name='entrance', blank=True, to='entrances.Entrance', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
