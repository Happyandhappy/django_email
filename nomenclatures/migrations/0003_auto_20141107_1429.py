# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0002_auto_20141107_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktype',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
            preserve_default=True,
        ),
    ]
