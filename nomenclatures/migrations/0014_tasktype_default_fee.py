# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0013_priority_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='default_fee',
            field=models.BooleanField(default=False, verbose_name='Default fee'),
            preserve_default=True,
        ),
    ]
