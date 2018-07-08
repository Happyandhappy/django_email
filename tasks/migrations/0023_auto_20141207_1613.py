# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import select2.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_auto_20141129_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='visit_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Visit date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='assignee',
            field=select2.fields.ForeignKey(verbose_name='Assignee', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='Entrance', blank=True, to='entrances.Entrance', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='can_pay',
            field=models.BooleanField(default=False, verbose_name='Can pay'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='can_pay_partial',
            field=models.BooleanField(default=False, verbose_name='Can pay partial'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='Entrance', blank=True, to='entrances.Entrance', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=select2.fields.ForeignKey(verbose_name='Priority', to='nomenclatures.Priority'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=select2.fields.ForeignKey(verbose_name='Task type', to='nomenclatures.TaskType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskdocument',
            name='document',
            field=models.FileField(upload_to=b'taskdocuments/%Y/%m', verbose_name='Document'),
            preserve_default=True,
        ),
    ]
