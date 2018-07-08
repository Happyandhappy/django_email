# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskdocument',
            options={'verbose_name': 'uploaded document', 'verbose_name_plural': 'uploaded documents'},
        ),
        migrations.RemoveField(
            model_name='task',
            name='documents',
        ),
        migrations.AddField(
            model_name='taskdocument',
            name='task',
            field=models.ForeignKey(default='', verbose_name='task', to='tasks.Task'),
            preserve_default=False,
        ),
    ]
