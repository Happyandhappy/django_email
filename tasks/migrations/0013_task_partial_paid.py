# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_remove_task_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='partial_paid',
            field=models.DecimalField(null=True, verbose_name='Partial paid', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
