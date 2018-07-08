# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0027_auto_20150120_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrance',
            name='position',
            field=models.IntegerField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
