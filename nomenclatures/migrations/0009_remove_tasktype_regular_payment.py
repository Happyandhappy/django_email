# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0008_tasktype_regular_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktype',
            name='regular_payment',
        ),
    ]
