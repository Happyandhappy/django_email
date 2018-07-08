# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'document', 'verbose_name_plural': 'documents'},
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=b'documents', verbose_name='document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='visible_to_groups',
            field=select2.fields.ManyToManyField(to='auth.Group', verbose_name='Visible to groups'),
            preserve_default=True,
        ),
    ]
