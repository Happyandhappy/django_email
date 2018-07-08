# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0009_remove_tasktype_regular_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='for_entrance_only',
            field=models.BooleanField(default=False, verbose_name='for entrance only'),
            preserve_default=True,
        ),
    ]
