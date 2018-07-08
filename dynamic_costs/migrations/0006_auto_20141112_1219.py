# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0005_dynamiccost_apartment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dynamiccost',
            old_name='apartment',
            new_name='apartments',
        ),
    ]
