# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0008_auto_20141110_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='apartment_integer',
            field=models.IntegerField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartment',
            name='apartment',
            field=models.CharField(max_length=255, verbose_name='Apartment'),
            preserve_default=True,
        ),
    ]
