# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0028_entrance_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrance',
            options={'ordering': ('-active', 'title'), 'verbose_name': 'Entrance', 'verbose_name_plural': 'Entrances'},
        ),
        migrations.AlterField(
            model_name='entrance',
            name='position',
            field=models.IntegerField(verbose_name='Position', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
