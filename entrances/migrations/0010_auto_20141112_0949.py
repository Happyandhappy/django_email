# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0009_auto_20141110_1309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'ordering': ('floor', 'apartment_integer'), 'verbose_name': 'Apartment', 'verbose_name_plural': 'Apartments'},
        ),
    ]
