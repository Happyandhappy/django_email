# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_task_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='template',
        ),
    ]
