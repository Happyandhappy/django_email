# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0006_auto_20141112_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='apartments',
            field=select2.fields.ManyToManyField(related_name='dynamic_costs', verbose_name='Apartments', to='entrances.Apartment'),
            preserve_default=True,
        ),
    ]
