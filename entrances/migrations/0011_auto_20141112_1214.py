# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0010_auto_20141112_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
    ]
