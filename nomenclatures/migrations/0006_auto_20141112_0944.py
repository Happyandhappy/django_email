# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0005_auto_20141110_1148'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Priorioty',
            new_name='Priority',
        ),
    ]
