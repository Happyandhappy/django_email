# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20141107_1425'),
        ('tasks', '0005_remove_task_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='template',
            field=select2.fields.ForeignKey(verbose_name='document', blank=True, to='documents.Document', null=True),
            preserve_default=True,
        ),
    ]
