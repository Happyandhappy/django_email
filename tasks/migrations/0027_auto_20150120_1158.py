# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0026_task_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'ordering': ('visit_date',), 'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 20, 9, 58, 10, 522496, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
