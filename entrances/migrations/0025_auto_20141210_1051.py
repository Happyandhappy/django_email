# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0024_entrance_tax_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrance',
            name='tax_amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='Tax amount description', null=True, verbose_name='Tax amount'),
            preserve_default=True,
        ),
    ]
