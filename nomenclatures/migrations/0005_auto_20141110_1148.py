# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0004_priorioty'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priorioty',
            options={'verbose_name': 'priority', 'verbose_name_plural': 'priorities'},
        ),
    ]
