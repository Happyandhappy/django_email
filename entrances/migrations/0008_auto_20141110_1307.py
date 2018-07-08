# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0007_auto_20141110_1302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'ordering': ('floor', 'apartment'), 'verbose_name': 'Apartment', 'verbose_name_plural': 'Apartments'},
        ),
        migrations.AlterField(
            model_name='apartment',
            name='apartment',
            field=models.IntegerField(max_length=255, verbose_name='Apartment'),
            preserve_default=True,
        ),
    ]
