# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrance',
            options={'verbose_name': 'entrance', 'verbose_name_plural': 'Entrances'},
        ),
        migrations.RemoveField(
            model_name='entrance',
            name='address',
        ),
    ]
