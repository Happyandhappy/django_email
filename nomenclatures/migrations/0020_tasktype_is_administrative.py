# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0019_auto_20151024_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='is_administrative',
            field=models.BooleanField(default=False, help_text='Will be shown as a separate sheet', verbose_name='Administrative Task'),
            preserve_default=True,
        ),
    ]
