# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0007_tasktype_price_for_resolve'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='regular_payment',
            field=models.BooleanField(default=False, verbose_name='regular payment'),
            preserve_default=True,
        ),
    ]
