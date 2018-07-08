# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0020_tasktype_is_administrative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktype',
            name='is_administrative',
            field=models.BooleanField(default=False, verbose_name='Administrative Task'),
            preserve_default=True,
        ),
    ]
