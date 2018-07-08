# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0014_tasktype_default_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktype',
            name='home_manager_fee',
            field=models.BooleanField(default=False, verbose_name='Home manager fee'),
            preserve_default=True,
        ),
    ]
