# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_document_editable_by_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=b'documents', verbose_name='Document'),
            preserve_default=True,
        ),
    ]
