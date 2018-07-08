# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0038_schedule_is_cachier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentahead',
            name='assignee',
            field=models.ForeignKey(blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='assignee',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='common_information',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
