# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_task_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='template',
            new_name='templates',
        ),
    ]
