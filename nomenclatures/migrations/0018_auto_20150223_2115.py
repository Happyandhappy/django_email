# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0017_auto_20141210_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasktype',
            options={'ordering': ('title',), 'verbose_name': 'Task type', 'verbose_name_plural': 'Task types'},
        ),
    ]
