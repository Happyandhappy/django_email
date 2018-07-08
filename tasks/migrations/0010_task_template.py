# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20141107_1425'),
        ('tasks', '0009_remove_task_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='template',
            field=models.ManyToManyField(to='documents.Document', null=True, verbose_name='document', blank=True),
            preserve_default=True,
        ),
    ]
