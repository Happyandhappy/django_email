# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0005_auto_20141110_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='entrance',
            field=select2.fields.ForeignKey(default='', to='entrances.Entrance'),
            preserve_default=False,
        ),
    ]
