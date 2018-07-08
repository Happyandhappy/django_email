# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_auto_20141114_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_paid',
        ),
    ]
