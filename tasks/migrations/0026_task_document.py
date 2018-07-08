# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0025_auto_20141210_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='document',
            field=models.FileField(upload_to=b'maintaskdocuments/%Y/%m', null=True, verbose_name='Document', blank=True),
            preserve_default=True,
        ),
    ]
