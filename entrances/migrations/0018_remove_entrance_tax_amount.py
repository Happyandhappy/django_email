# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0017_auto_20141121_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrance',
            name='tax_amount',
        ),
    ]
