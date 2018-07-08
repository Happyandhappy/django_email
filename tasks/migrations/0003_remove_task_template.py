# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20141113_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='template',
        ),
    ]
