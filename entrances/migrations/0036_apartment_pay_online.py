# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0035_auto_20151024_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='pay_online',
            field=models.BooleanField(default=False, verbose_name='Pay online'),
            preserve_default=True,
        ),
    ]
