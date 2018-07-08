# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_auto_20141121_0835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='dynamic_cost',
        ),
    ]
