# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0011_auto_20141112_1214'),
        ('dynamic_costs', '0004_auto_20141112_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamiccost',
            name='apartment',
            field=select2.fields.ManyToManyField(to='entrances.Apartment', verbose_name='Apartments'),
            preserve_default=True,
        ),
    ]
