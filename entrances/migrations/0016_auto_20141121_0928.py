# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0015_auto_20141121_0925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='monthly_expences',
        ),
        migrations.RemoveField(
            model_name='monthlyexpence',
            name='apartment',
        ),
    ]
