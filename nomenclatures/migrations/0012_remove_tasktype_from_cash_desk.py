# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0011_auto_20141118_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktype',
            name='from_cash_desk',
        ),
    ]
