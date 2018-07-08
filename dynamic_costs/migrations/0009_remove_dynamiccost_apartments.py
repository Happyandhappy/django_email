# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0008_auto_20141112_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamiccost',
            name='apartments',
        ),
    ]
