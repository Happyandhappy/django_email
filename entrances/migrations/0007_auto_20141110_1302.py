# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0006_apartment_entrance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='common_information',
            field=models.TextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
